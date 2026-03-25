from core.base_controller import BaseController


class AuthController(BaseController):
    def __init__(self):
        super().__init__()

    def index(self):
        return self.render("start.html")
