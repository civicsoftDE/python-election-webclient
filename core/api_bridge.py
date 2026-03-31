from typing import ClassVar


class ApiBridge:
    headers: ClassVar[dict] = {
        "Content-Type": "application/json"
    }

    def __init__(self, verify_ssl_certs: bool = True):
        self._verify_ssl_certs = verify_ssl_certs

    def request(self, url: str, data: dict) -> dict:
        pass

    def respond(self, url: str, data: dict) -> int:
        pass
