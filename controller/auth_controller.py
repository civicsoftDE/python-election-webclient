from core.base_controller import BaseController
from core.route import route


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self):
        if not self.has_current_user():
            return self.redirect_to_route("auth_login")
        return self.render("start")

    @route('auth_login')
    def login(self, slot_id: str = None, password: str = None):
        if self.has_current_user():
            return self.redirect_to_route("auth_index")
        if slot_id and password:
            session = self.get_crypto_bridge().login(slot_id, password)
            if session is not None:
                self.set_current_user()
                session.closeSession()
                self.add_flash("Login erfolgreich")
                return self.redirect_to_route("auth_index")
            else:
                self.add_flash("Login fehlgeschlagen", "danger")  # default ist immer "success"
        return self.render_login()

    @route('auth_logout')
    def logout(self):
        if self.has_current_user():
            self.clear_user()
            self.add_flash("Logout erfolgreich")
        return self.redirect_to_route("auth_login")
