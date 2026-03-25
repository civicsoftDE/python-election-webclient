import json

from PySide6.QtCore import QObject, Slot

from core.router import Router


class BackendBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.router = Router()

    @Slot(str, result=str)
    def load_view(self, route_name: str):
        """Wird von JavaScript aufgerufen: loadView('election_index')"""
        try:
            html = self.router.execute(route_name)
            return html
        except Exception as e:
            print(f"Router Error: {e}")
            # Fallback: Error-View rendern
            from controller.error_controller import ErrorController
            return ErrorController().render("error.html", {"error": str(e)})