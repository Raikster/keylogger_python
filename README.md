# keylogger_python
 Das Keylogger Projekt für die vorliegende MasterThesis soll zeigen, dass ein Seitenkanalangriff auf das Verschlüsselungspasswort innerhalb von Windows möglich ist.

# Voraussetzungen
Windows + Lauffähige Python3 Installation
für das Python Keyloggerskript werden folgende Pip Module benötigt:
- keyboard
- pywin32
für das Serverskript werden keine gesonderten Pipmodule benötigt.

# Benutzung
Der Keylogger steht in 3 Formaten bereit: 
Das reguläre .py Skript läuft in der cmd und ermöglicht das Nachverfolgen der Outputs.
Das .pyw Skript ist vom Code identisch mit dem .py Skript. Mit dem Unterschied, dass der Code ausgeführt wird ohne dass das Kommandozeilenfenster aufspringt.
Im Ordner keylogger.zip ist der Keylogger als Exe enthalten. Das Passwort zum entpacken ist "123". Der Keylogger wird vom Windows Defender als Trojaner erkannt, die Heuristiken funktionieren also. Die Exe wurde mit Hilfe von Pyinstaller erstellt und ist eine gebundelte Umgebung in dem alle Python notwendigen Funktionen und Abhängigkeiten enthalten sind. das hießt die Exe ist aktuell nur über die Kommandozeile benutzbar.

# Workflow
Das Skript beinhaltet folgenden Workflow:
1. Deklaration der Variablen für das spätere check & copy in den versteckten Ordner und dem Windows Autostart Ordner
2. Prüfen ob der versteckte Ordner %User%\.keylog angelegt wurde, falls nicht Ordner erstellen
3. Prüfen ob die gerade ausgeführte Datei aus dem versteckten Ordner ausgeführt wird, falls nicht kopieren dorthin
4. Prüfen ob die ausgeführte Datei eine .exe oder ein .py Skript ist und Info in die Variable "f_extension" schreiben
5. Falls nicht vorhanden, erstelle eine Verknüpfung zur ausgeführten Datei im versteckten Ordner
6. Start des Keyloggers - Alle 60s schreiben einer Textdatei und senden der Textdatei an einen Server

# Error Handling
Es ist ein rudimentäres Errorhandling implementiert, dass die schwerwiegensten Fehler abfängt.

# ToDo
1. Sicherstellung der Ausführung im Hintergrund wenn das Skript/Exe während des Autostart geladen wird
2. Schreiben der Textdatei nicht in den aktuellen Ordner des ausgeführten Skripts/Exe sondern in den versteckten Ordner
3. Kompilieren der Exe im Window Mode, so dass die Exe als Hintergrundprozess laufen kann
4. Kennzeichnen des Quellcodes nach eigenem Code und Fremdcode

# Ergebnisse
Was kann das softwarebasierte Logging leisten?
Die bereitgestellten Dateien zeigen, dass die Tastatureingaben aufgenommen und weiter an einen Server gesendet werden können. Da der softwarebasierte Keylogger frühestens mit dem Windows Start initialisiert werden kann, kann der Verschlüsselungskey der beim Booten eingegeben werden muss nicht geparst werden. Ebenso wenig können Verschlüsselungskeys die aus dem TPM direkt an die CPU übergeben werden (bspw. für verschlüsselte Zweitlaufwerke) nicht mitgeschnitten werden. Der Keylogger erfordert daher Programme die eine aktive Tastatureingabe per Passwort abfordern.
