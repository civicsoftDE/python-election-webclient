from typing import ClassVar

from jinja2 import Environment

from core.bootstrap import Bootstrap
from core.pkcs11_bridge import PKCS11Bridge
from core.qrc_loader import QrcLoader
from model.user import User


class BaseController:
    default_context: ClassVar[dict] = {
        "app": {
            "user": None
        }
    }

    def __init__(self):
        self.loader = QrcLoader()
        self.env = Environment(loader=self.loader)

    def set_user(self, user: User | None):
        self.default_context["app"]["user"] = user

    def set_current_user(self):
        self.default_context["app"]["user"] = self.get_crypto_bridge().current_user

    def has_current_user(self) -> bool:
        return self.get_crypto_bridge().current_user is not None

    def clear_user(self):
        self.get_crypto_bridge().current_user = None
        self.default_context["app"]["user"] = None

    def get_main_window(self):
        return Bootstrap.get_instance()

    def get_crypto_bridge(self) -> PKCS11Bridge:
        return self.get_main_window().pkcs11_bridge

    def render(self, view_name: str, context: dict = None) -> str:
        if context is None:
            context = {}
        if not view_name.endswith('.html.j2'):
            view_name += '.html.j2'
        template = self.env.get_template("templates/" + view_name)
        render_context = {**self.default_context, **context}
        return template.render(**render_context)
