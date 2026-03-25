from core.base_controller import BaseController


class AuthController(BaseController):
    def index(self, id: int = None):
        if id is None:
            return self.render("start.html.j2")
        else:
            return self.render("start", {
                "id": id
            })
