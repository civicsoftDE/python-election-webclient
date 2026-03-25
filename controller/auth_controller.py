from core.base_controller import BaseController
from core.route import route


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self, id: int = None):
        data = {}
        if id is not None:
            data["id"] = id
        return self.render("start", data)
