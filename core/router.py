import importlib
from pathlib import Path

import yaml


class Router:
    def __init__(self, config_path: str = "config/routes.yaml"):
        with open(Path(config_path), 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.routes = config.get('routes', {})
        self._controller_cache = {}

    def _get_controller_class(self, controller_name: str):
        """Lädt Controller-Klasse dynamisch (mit Cache)"""
        if controller_name in self._controller_cache:
            return self._controller_cache[controller_name]

        # AuthController → auth_controller.py
        module_name = self._camel_to_snake(controller_name)
        module = importlib.import_module(f"controller.{module_name}")
        controller_class = getattr(module, controller_name)
        self._controller_cache[controller_name] = controller_class
        return controller_class

    def _camel_to_snake(self, name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def execute(self, route_name: str, **kwargs) -> str:
        """
        Führt Route aus und returnt HTML.
        Wird von der Bridge aufgerufen.
        """
        if route_name not in self.routes:
            raise ValueError(f"Route '{route_name}' nicht gefunden")
        route_config = self.routes[route_name]
        controller_name, method_name = route_config.split('::')
        controller_class = self._get_controller_class(controller_name)
        controller = controller_class()
        method = getattr(controller, method_name)
        return method(**kwargs)
