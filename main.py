import sys
from pathlib import Path

import resources_rc

from PySide6.QtWidgets import QApplication

from core.bootstrap import Bootstrap

WINDOW_ICON = "chart2.ico"
ICON_PATH = "resources/static/icons/"


def get_resource_path(relative_path):
    """
    Gibt den absoluten Pfad zurück – funktioniert sowohl in der
    Entwicklung als auch im PyInstaller Build.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller Build
        base_path = Path(sys._MEIPASS)
    else:
        # Entwicklung / Normaler Python Start
        base_path = Path(__file__).parent
    return base_path / relative_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Bootstrap().show()
    sys.exit(app.exec())
