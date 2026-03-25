from functools import wraps


class Route:
    """
    Decorator für Controller-Methoden
    Verwendung: @route("election_index")
    """
    _registry = {}  # Zentrale Route-Registry (Singleton)

    def __init__(self, name: str):
        self.name = name

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Route registrieren
        self._registry[self.name] = {
            "func": func,
            "name": self.name,
            "module": func.__module__,
            "controller": func.__qualname__.split('.')[0]
        }

        return wrapper

    @classmethod
    def get_registry(cls) -> dict:
        """Gibt alle registrierten Routes zurück"""
        return cls._registry.copy()

    @classmethod
    def clear_registry(cls):
        """Löscht alle registrierten Routes (für Tests)"""
        cls._registry = {}


# Shortcut für einfacheren Import
route = Route
