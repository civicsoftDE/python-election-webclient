class Route:
    _registry = {}

    def __init__(self, name: str, aliases: list = None):
        """
        Route-Decorator mit Alias-Support

        Args:
            name: Haupt-Name der Route
            aliases: Liste von Alias-Namen (optional)
        """
        self.name = name
        self.aliases = aliases or []

    def __call__(self, func):
        route_info = {
            "func": func,
            "method_name": func.__name__,
            "name": self.name,
            "module": func.__module__,
            "controller": func.__qualname__.split('.')[0] if '.' in func.__qualname__ else 'Unknown',
            "aliases": self.aliases
        }
        self._registry[self.name] = route_info
        for alias in self.aliases:
            self._registry[alias] = route_info
        return func

    @classmethod
    def get_registry(cls) -> dict:
        """Gibt eine Kopie der Registry zurück"""
        return cls._registry.copy()

    @classmethod
    def clear_registry(cls):
        """Löscht alle registrierten Routes (für Tests)"""
        cls._registry = {}

    @classmethod
    def get_route_info(cls, route_name: str) -> dict:
        """Gibt Information für eine spezifische Route zurück"""
        return cls._registry.get(route_name)

    @classmethod
    def get_all_routes(cls) -> list:
        """Gibt alle Route-Namen zurück (inkl. Aliase)"""
        return list(cls._registry.keys())

    @classmethod
    def get_main_routes(cls) -> list:
        """Gibt nur Haupt-Routes zurück (ohne Aliase)"""
        return [
            name for name, info in cls._registry.items()
            if info["name"] == name
        ]


route = Route
