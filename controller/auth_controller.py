from core.base_controller import BaseController
from core.route import route


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self):
        if not self.has_current_user():
            return self.render_login()
        return self.render("start")

    @route('auth_login')
    def login(self, slot_id: str, password: str):
        if self.has_current_user():
            return self.index()
        session = self.get_crypto_bridge().login(slot_id, password)
        if session is not None:
            self.set_current_user()
            session.closeSession()
            return self.render("start")
        else:
            return self.render_login()

    @route('auth_logout')
    def logout(self):
        if self.has_current_user():
            self.clear_user()
        return self.render_login()