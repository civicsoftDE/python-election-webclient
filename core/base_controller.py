from jinja2 import Environment

from core.qrc_loader import QrcLoader


class BaseController:
    def __init__(self):
        self.loader = QrcLoader()
        self.env = Environment(loader=self.loader)
        self.default_context = {
            "message_header": "Ausweis einlegen",
            "message_explanation": "Bitte legen Sie Ihren Personalausweis auf das Lesegerät."
        }

    def render(self, view_name: str, context: dict = None) -> str:
        if context is None:
            context = {}
        if not view_name.endswith('.html.j2'):
            view_name += '.html.j2'
        template = self.env.get_template("templates/" + view_name)
        self.default_context.update(context)
        render_context = {**self.default_context, **context}
        return template.render(**render_context)
