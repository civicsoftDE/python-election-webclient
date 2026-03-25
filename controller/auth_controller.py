from PySide6.QtWidgets import QMessageBox

from core.base_controller import BaseController
from core.route import route


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self, id: int = None):
        data = {}
        accept = False
        if id is not None:
            data["id"] = id
            reply = QMessageBox.question(
                self.get_main_window(),
                "Stimme abgeben",
                f"Möchten Sie zustimmen?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                accept = True
        data["accept"] = accept
        return self.render("start", data)

    @route('result')
    def results(self):
        return self.render("result")