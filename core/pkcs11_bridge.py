import os
from typing import ClassVar

import PyKCS11
from PyKCS11 import Session

from core.config import AppConfig
from model.user import User


class PKCS11Bridge:
    current_user = None

    def __init__(self, config: AppConfig):
        self.slots = []
        self._config = config
        os.environ['SOFTHSM2_CONF'] = self._config.get('pkcs11.conf')
        self._pkcs11lib = PyKCS11.PyKCS11Lib()
        self._pkcs11lib.load(self._config.get('pkcs11.lib'))
        self._init_slots()

    def get_slots(self) -> list[User]:
        return self.slots

    def login(self, slot_id, pin) -> Session | None:
        session = None
        try:
            slot_id_int = int(slot_id)
            session = self._pkcs11lib.openSession(
                slot_id_int,
                PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION
            )
            session.login(pin)
            token_info = self._pkcs11lib.getTokenInfo(slot_id_int)
            label = getattr(token_info, 'label', '').strip()
            serial = getattr(token_info, 'serialNumber', '').strip()
            self.current_user = User(id=slot_id, label=label, serial=serial)
            return session
        except PyKCS11.PyKCS11Error as e:
            if "CKR_PIN_INCORRECT" in str(e) or "CKR_PIN_INVALID" in str(e):
                print("❌ Falsche PIN!")
            elif "CKR_USER_ALREADY_LOGGED_IN" in str(e):
                print("ℹ️ Bereits eingeloggt")
            else:
                print(f"PIN-Fehler: {str(e)[:50]}")
            if session:
                session.closeSession()
            return None

    def logout(self):
        self.current_user = None

    def _init_slots(self):
        slots = self._pkcs11lib.getSlotList(tokenPresent=True)
        initialized_count = 0

        for slot_id in slots:
            try:
                token_info = self._pkcs11lib.getTokenInfo(slot_id)
                label = getattr(token_info, 'label', '').strip()
                if not label:
                    continue
                serial = getattr(token_info, 'serialNumber', '').strip()
                self.slots.append(User(id=slot_id, label=label, serial=serial))
                initialized_count += 1

            except PyKCS11.PyKCS11Error:
                continue
