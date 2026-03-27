from core.base_controller import BaseController
from core.route import route


class ResultController(BaseController):

    @route('result')
    def results(self):
        return self.render("result")
