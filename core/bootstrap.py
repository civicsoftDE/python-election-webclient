import PySide6
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow

from core.backend_bridge import BackendBridge
from core.config import AppConfig
from core.pkcs11_bridge import PKCS11Bridge


class Bootstrap(QMainWindow):
    _instance = None

    def __init__(self):
        super().__init__()
        Bootstrap._instance = self
        self.config = AppConfig()
        self.pkcs11_bridge = PKCS11Bridge(self.config)
        self.bridge = BackendBridge(self)
        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self._init_window()
        self._init_web_engine()
        self._init_web_channel()

        self.load_view('start')

    @classmethod
    def get_instance(cls):
        return cls._instance

    def load_view(self, view_name: str):
        self.bridge.load_view(view_name)

    def _init_window(self):
        # Fenster-Titel
        self.setWindowTitle(self.config.app_name)
        # Fenster-Icon
        self.setWindowIcon(QIcon(self.config.get('window.icon')))
        # Fenster-Größe
        self.resize(
            self.config.get('window.width', 1280),
            self.config.get('window.height', 720)
        )
        # Minimum-Größe
        self.setMinimumWidth(self.config.get('window.min_width', 1280))
        self.setMinimumHeight(self.config.get('window.min_height', 720))

    def _init_web_engine(self):

        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.setCentralWidget(self.browser)

    def _init_web_channel(self):
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)
