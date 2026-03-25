from pathlib import Path

import yaml


class AppConfig:
    _instance = None
    _config = {}

    def __new__(cls):
        """Singleton Pattern – nur eine Instanz"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self._config = self._load_config()

    def _load_config(self) -> dict:
        """Lädt config/app.yaml"""
        config_path = Path(__file__).parent.parent / "config" / "app.yaml"

        # Für PyInstaller Build
        import sys
        if hasattr(sys, '_MEIPASS'):
            config_path = Path(sys._MEIPASS) / "config" / "app.yaml"

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def get(self, key: str, default=None):
        """
        Holt einen Wert mit Dot-Notation
        config.get('app.name') → "Wahlsoftware"
        config.get('window.width') → 1280
        """
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    @property
    def app_name(self) -> str:
        return self.get('app.name', 'Wahlsoftware')

    @property
    def app_version(self) -> str:
        return self.get('app.version', '1.0.0')

    @property
    def organization(self) -> str:
        return self.get('app.organization', 'Unknown')
