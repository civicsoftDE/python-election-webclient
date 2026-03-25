from PySide6.QtCore import QIODevice, QFile
from jinja2 import BaseLoader, TemplateNotFound


class QrcLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def get_source(self, environment, template_path):
        if template_path in self.cache:
            return self.cache[template_path]
        file = QFile(f":/{template_path}")
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            raise TemplateNotFound(template_path)
        source = file.readAll().data().decode("utf-8")
        file.close()
        uptodate = lambda: True
        self.cache[template_path] = (source, template_path, uptodate)
        return self.cache[template_path]
