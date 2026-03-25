# Pyhton QT Election-Client

## Installation

### Update Templates
````shell
pyside6-rcc resources/resources.qrc -o resources_rc.py
````

### Create Specs
````shell
pyi-makespec --windowed --name "Wahlsoftware" main.py 
````

### Build Application
````shell
pyinstaller Wahlsoftware.spec  
````