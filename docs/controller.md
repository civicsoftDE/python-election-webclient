# Controller

## Aufbau und Struktur

Controller in dieser Anwendung folgen dem Fat Controller Pattern.
Jeder Controller erbt vom ``BaseController`` und übernimmt die Darstellung der Geschäftslogik.

### Grundstruktur

````python
from core.base_controller import BaseController

class ExampleController(BaseController):
    def __init__(self):
        super().__init__()
    
    def index(self):
        return self.render("example_index")
    
    def detail(self, id: int):
        return self.render("example_detail", {
            "id": id,
            "title": "Detail-Ansicht"
        })
````

## BaseController

Jeder Controller erbt automatisch vom BaseController. Dieser stellt folgende Funktionen bereit:

``render(view_name: str, context: dict = None) -> str``

Rendert ein Jinja2-Template und gibt den HTML-String zurück.