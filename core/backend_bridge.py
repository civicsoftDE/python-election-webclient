from PySide6.QtCore import QObject, Slot

from core.router import Router


class BackendBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.router = Router()
        self.router.discover_routes()

    @Slot(str, 'QVariant', result=str)
    def load_view(self, route_name: str, data: dict = None):
        """Wird von JavaScript aufgerufen: loadView('election_index')"""
        try:
            if data is None:
                data = {}
            return self.router.execute(route_name, **data)
        except Exception as e:
            print(f"Router Error: {e}")
            from core.error_controller import ErrorController
            return ErrorController().render("error", {"error": str(e)})
