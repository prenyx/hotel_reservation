---
Business_Name:Business Artificial IntelligenceModule_Info:   
Name: Anwendungsentwicklung mit Python  
Authors:        
  - Supavadee Theerapong    
  - Manuel Pasamontes    
  - Damian Martin    
  - Steven Chevalley
---
---
**Bsc Business Artificial Intelligence** Modul: Anwendungsentwicklung mit Python

**Projektdokumentation**: Hotelreservierungssystem

**Autoren**: *Gruppe B* (Supavadee Theerapong, Manuel Passamontes, Damian Martin, Steven Chevalley) 

---
# 1. Einführung
Das vorliegende Projekt ist Teil des Moduls, das darauf abzielt, die Konzepte der Programmierung mithilfe 
der Programmiersprache **Python** praxisnah zu erlernen. Im Rahmen dieses Projekts wird ein *Hotelreservierungssystem* 
entwickelt. Ziel ist es, den Studierenden die Möglichkeit zu bieten, theoretische Programmierkenntnisse auf ein 
realistisches Anwendungsszenario anzuwenden und dabei wichtige praktische Erfahrungen zu sammeln.

# 2. Systemarchitektur
Das Hotelreservierungssystem ist eine umfassende Lösung 
zur Verwaltung von Hotelbuchungen, die auf Python basiert und 
**SQLAlchemy** als ORM (Object-Relational Mapping) verwendet. 
Die Architektur des Systems ist modular aufgebaut, wobei jede 
Hauptfunktionalität in einem eigenen Modul implementiert ist. 
Diese Struktur fördert die Wartbarkeit und Erweiterbarkeit des Systems.

## 2.1 Hauptkomponenten des Systems
1. **Benutzerverwaltung**
   - *Beschreibung*: Das Benutzerverwaltungssystem behandelt die Registrierung, Authentifizierung 
   und Autorisierung von Benutzern. Es gibt zwei Haupttypen von Benutzern: Gäste und registrierte Gäste.
   - *Entitäten*:
     - Role: Definiert die Rolle eines Benutzers und den entsprechenden Zugriff.
     - Login: Enthält Anmeldedaten und verknüpft Benutzerrollen.

2. **Gastverwaltung**
   - *Beschreibung*: Dieses Modul verwaltet die Informationen der Gäste, einschliesslich ihrer persönlichen Daten und Adressen.
   - *Entitäten*:
     - Guest: Basisinformationen zu Gästen
     - RegisteredGuest: Erweiterung von Guest mit Login-Daten für registrierte Gäste.
     - Address: Speichert Adressen der Gäste.

3. **Hotel- und Zimmerverwaltung**
   - *Beschreibung*: Verwaltung von Hotelinformationen und Zimmerdetails, einschließlich Verfügbarkeit und spezifischen Zimmermerkmalen.
   - *Entitäten*:
     - Hotel: Informationen zu Hotels, einschließlich Name, Sternebewertung und Adresse.
     - Room: Details zu den Zimmern, einschließlich Zimmernummer, Typ, Preis und Verfügbarkeit.

4. **Buchungsverwaltung**:
   - *Beschreibung*: Dieses Modul kümmert sich um die Verwaltung von Zimmerbuchungen, einschließlich der Verknüpfung von 
   Gästen und Zimmern sowie der Buchungsdetails.
   - *Entitäten*: 
     - Booking: Speichert Informationen zu Buchungen, einschließlich Datum, 
     Anzahl der Gäste und Zimmerdetails.

## 2.2 Verwendete Technologien und Tools
Dieses Projekt wurde mit Python 3.12 entwickelt. 
Python wurde aufgrund seiner Einfachheit, Lesbarkeit und der breiten Unterstützung durch eine Vielzahl von Bibliotheken 
und Frameworks gewählt.
Für die Datenbankimplementierung wurde wie bereits erwähnt SQLAlchemy verwendet, 
eine leistungsfähige Bibliothek, die die Arbeit mit relationalen Datenbanken vereinfacht und gleichzeitig leistungsfähige ORM-Funktionalitäten bietet.

### 2.2.1 Entwicklungs- und Kollaborationstools
Für die Versionskontrolle und Zusammenarbeit im Team wurde GitHub eingesetzt. 
GitHub ermöglicht eine nahtlose Verwaltung von Quellcodeänderungen und unterstützt das Team bei der Verfolgung des Entwicklungsfortschritts. 
Zu den genutzten Funktionen gehören:
- **Version Control**: Verwalten von Quellcodeänderungen und Nachverfolgen des Entwicklungsverlaufs. 
- **Issues und Pull Requests**: Organisieren von Aufgaben, Durchführen von Code-Reviews und Sicherstellen der Code-Qualität. 
- **GitHub Projects**: Nutzen des integrierten Kanban-Boards zur Aufgabenverwaltung und Projektplanung.

Als integrierte Entwicklungsumgebung (IDE) wurde PyCharm verwendet. PyCharm bietet eine Vielzahl von Funktionen wie Code-Vervollständigung, 
Debugging und Versionskontrolle, die die Entwicklungsarbeit erheblich erleichtern. 
Die direkte Integration mit GitHub ermöglicht eine effiziente Versionsverwaltung und Zusammenarbeit direkt aus der IDE heraus.

### 2.2.2 Projektmanagement
Zur Verwaltung und Visualisierung der Aufgaben sowie des Projektfortschritts wird ein **Kanban-Board**
verwendet. Dieses Tool ermöglicht es dem Team, alle anstehenden, in Bearbeitung befindlichen 
und abgeschlossenen Aufgaben übersichtlich darzustellen. Durch die visuelle Darstellung kann 
das Team den Arbeitsfluss effizienter organisieren, Engpässe schnell identifizieren und die 
Produktivität steigern. Das Kanban-Board unterstützt somit eine transparente und flexible 
Projektplanung, die es dem Team erlaubt, kontinuierlich Verbesserungen vorzunehmen und auf 
Änderungen agil zu reagieren.

### 2.2.3 Testing und Debugging (Manuel Ergänze?)
Das System wird lokal auf den Entwicklerrechnern ausgeführt und getestet. 
Aufgrund von Zeitbeschränkungen wurden keine umfassenden Unit-Tests geschrieben. 
Stattdessen wurde die Funktionalität direkt in den jeweiligen Dateien durch ein `if __name__ == "__main__":`-Block getestet. 
Diese Methode ermöglichte es den Entwicklern, einzelne Module schnell und effizient zu testen, indem sie spezifische Testfälle direkt in den Hauptprogrammbereich der Datei einfügten. Trotz der fehlenden formalen Unit-Tests konnten so die grundlegenden Funktionen und die Interaktion der verschiedenen Komponenten sichergestellt werden.

# 3. Implementierungsdetail
Das Hotelreservierungssystem besteht aus mehreren Modulen, 
die jeweils spezifische Funktionen zur Verwaltung von Hotels, Zimmern, Buchungen und 
Benutzern bieten. Die Struktur des Projekts ist in verschiedene Ordner unterteilt, 
die die verschiedenen Aspekte des Systems abdecken. Die Dateien im Ordner `data_models` wurden 
von den Dozenten vorgegeben, ebenso wie die Dateien im Ordner `data_access` und `console`. 
Die Implementierung der Geschäftslogik im Ordner business wurde von den Studierenden selbst codiert.

- Detaillierte Beschreibung der implementierten Funktionen
- Code-Beispiele und Erklärungen

# 4. Datenbankdesign
Das Datenbankdesign für das Hotelreservierungssystem basiert auf einem **Entity-Relationship-Modell** (ER-Modell), 
das die verschiedenen Entitäten und ihre Beziehungen beschreibt. 
Das ER-Modell wurde von den Dozenten bereitgestellt und bildet die Grundlage für die Implementierung des Systems. 
Obwohl wir anfangs Überlegungen angestellt haben, das Modell zur Unterstützung einer dynamischeren Suchfunktion zu verbessern, 
haben wir letztendlich beschlossen, das vorgegebene Modell unverändert zu lassen, um die Einfachheit und Konsistenz zu gewährleisten.
- Beschreibung der Datenbanktabellen und -beziehungen

# 5. Lessons Learned
- Zusammenfassung der in den Interviews besprochenen Punkte
- Reflexionen der Teammitglieder über das Projekt und die gelernten Konzepte

- Während der Implementierung von UserManager.py fiel auf, dass die User Stories für Gastnutzer und registrierte Benutzer unklar formuliert waren. Um diese Unklarheiten zu beheben, entschieden wir uns, im User-Manager zwei grundlegende Methoden zu verwenden: “create_new_login” für die Erstellung neuer Logins und “register_existing_user” zum Hinzufügen von Benutzerdetails zu einem bestehenden Login.
Nach Rücksprache mit den Coaches stellte sich heraus, dass die User Stories und das Datenbankmodell zu einer grösseren Interpretationsspielraum hatten als bisher angedacht und wir eine alternative Herangehensweise gewählt hatten. Wir behielten den User-Manager mit der erweiterten Funktionalität bei, setzten jedoch die Arbeit am Reservationsmanager gemäss der Vision der Coaches fort.


