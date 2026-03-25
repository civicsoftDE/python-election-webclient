import importlib
import traceback
from pathlib import Path

from core.route import Route


class Router:
    def __init__(self, controllers_path: str = "controller"):
        self.controllers_path = Path(controllers_path)
        self._routes = None
        self._controller_cache = {}

    def _get_controller_class(self, controller_name: str):
        """Lädt Controller-Klasse dynamisch (mit Cache)"""
        if controller_name in self._controller_cache:
            return self._controller_cache[controller_name]
        module_name = self._camel_to_snake(controller_name)
        module = importlib.import_module(f"controller.{module_name}")
        controller_class = getattr(module, controller_name)
        self._controller_cache[controller_name] = controller_class
        return controller_class

    def _camel_to_snake(self, name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def discover_routes(self):
        """Scannt alle Controller-Dateien und registriert Routes automatisch"""
        if not self.controllers_path.exists():
            print(f"Controller-Pfad nicht gefunden: {self.controllers_path.absolute()}")
            return
        for controller_file in self.controllers_path.glob("*.py"):
            if controller_file.name.startswith("_"):
                continue
            module_name = f"controller.{controller_file.stem}"
            try:
                importlib.import_module(module_name)
            except Exception as e:
                print(f"Fehler beim Laden von {module_name}: {e}")
                traceback.print_exc()
        self._routes = Route.get_registry()

    def get_all_routes(self) -> list:
        return list(self._routes.keys())

    def execute(self, route_name: str, **kwargs) -> str:
        """
        Führt Route aus und returnt HTML.
        Wird von der Bridge aufgerufen.
        """
        if route_name not in self._routes:
            raise ValueError(f"Route '{route_name}' nicht gefunden")
        route_config = self._routes[route_name]
        controller_name = route_config.get('controller')
        method_name = route_config.get('method_name')
        controller_class = self._get_controller_class(controller_name)
        controller = controller_class()
        method = getattr(controller, method_name)
        return method(**kwargs)
