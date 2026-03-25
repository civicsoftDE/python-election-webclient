from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow

from core.backend_bridge import BackendBridge


class Bootstrap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bridge = BackendBridge(self)
        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self._init_window()
        self._init_web_engine()
        self._init_web_channel()
        self.load_view('start')

    def load_view(self, view_name: str):
        html = self.bridge.load_view(view_name)
        self.browser.setHtml(html, QUrl("qrc:///"))

    def _init_window(self):
        self.setWindowTitle("CivicSoft Germany")
        self.setWindowIcon(QIcon(":static/icons/chart2.ico"))
        self.resize(1280, 720)
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)

    def _init_web_engine(self):
        self.setCentralWidget(self.browser)
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)

    def _init_web_channel(self):
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)
