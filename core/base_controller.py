from typing import ClassVar

from jinja2 import Environment

from core.bootstrap import Bootstrap
from core.pkcs11_bridge import PKCS11Bridge
from core.qrc_loader import QrcLoader
from model.user import User


class BaseController:
    default_context: ClassVar[dict] = {
        "app": {
            "user": None,
            "flash_messages": []
        }
    }
    flash_messages: ClassVar[list] = []

    def __init__(self):
        self.loader = QrcLoader()
        self.env = Environment(loader=self.loader)

    def add_flash(self, flash_message: str, alert_type: str = "success"):
        self.flash_messages.append({
            "message": flash_message,
            "type": alert_type
        })

    def get_flashes(self) -> list:
        flash_list = list(self.flash_messages)
        self.flash_messages.clear()
        return flash_list

    def set_user(self, user: User | None):
        self.default_context["app"]["user"] = user

    def set_current_user(self):
        self.default_context["app"]["user"] = self.get_crypto_bridge().current_user

    def has_current_user(self) -> bool:
        return self.get_crypto_bridge().current_user is not None

    def clear_user(self):
        self.get_crypto_bridge().current_user = None
        self.default_context["app"]["user"] = None

    def get_main_window(self) -> Bootstrap:
        return Bootstrap.get_instance()

    def get_crypto_bridge(self) -> PKCS11Bridge:
        return self.get_main_window().pkcs11_bridge

    def redirect_to_route(self, route_name: str, context: dict = None) -> None:
        if context is None:
            context = {}
        return self.get_main_window().bridge.router.execute(route_name, **context)

    def render(self, view_name: str, context: dict = None) -> str:
        if context is None:
            context = {}
        if not view_name.endswith('.html.j2'):
            view_name += '.html.j2'
        template = self.env.get_template("templates/" + view_name)
        render_context = {**self.default_context, **context}
        self.default_context["app"]["flash_messages"].clear()
        render_context["app"]["flash_messages"] = self.get_flashes()
        return template.render(**render_context)

    def render_login(self):
        return self.render("login", {
            "slots": self.get_crypto_bridge().get_slots()
        })
