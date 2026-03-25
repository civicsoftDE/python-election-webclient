# Pyhton QT Election-Client

## Update Templates

````shell
pyside6-rcc resources/resources.qrc -o resources_rc.py
````

````shell
pyi-makespec --windowed --name "Wahlsoftware" main.py 
````

````shell
pyinstaller Wahlsoftware.spec  
````