from core.base_controller import BaseController
from core.route import route


class AuthController(BaseController):

    @route('auth_index', aliases=['start'])
    def index(self, id: int = None):
        if id is None:
            return self.render("start.html.j2")
        else:
            return self.render("start", {
                "id": id
            })
