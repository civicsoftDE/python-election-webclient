from PySide6.QtWidgets import QMessageBox

from core.base_controller import BaseController
from core.route import route
from model.user import User


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self, id: int = None):
        data = {}
        accept = False
        slots = self.get_crypto_bridge().get_slots()

        if self.has_current_user():
            print("Du bist eingeloggt!!!")

        if id is not None:
            data["id"] = id
            reply = QMessageBox.question(
                self.get_main_window(),
                "Stimme abgeben",
                f"Möchten Sie zustimmen?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.set_user(User("123", "456", "789"))
                print("YES")
                accept = True
            else:
                self.clear_user()
        data["accept"] = accept
        data["slots"] = slots
        session = self.get_crypto_bridge().login(slots[0].id, "1234")
        if session is not None:
            print("Sie sind eingeloggt und können signieren!")
            session.closeSession()

        return self.render("login", data)

    @route('auth_login')
    def login(self, slot_id: str, password: str):
        print(f"ID: {slot_id}")
        session = self.get_crypto_bridge().login(slot_id, password)
        if session is not None:
            print("Login Okay!")
            self.set_current_user()
            session.closeSession()
            if self.has_current_user():
                print("Du bist eingeloggt!!!")
            return self.render("start")
        else:
            print("Login Falsch!")
            self.clear_user()
            return self.render("login", {
                "slots": self.get_crypto_bridge().get_slots()
            })
