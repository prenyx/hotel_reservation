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

- Detaillierte Beschreibung der implementierten Funktionen (brauchen wir das)
- Code-Beispiele und Erklärungen

## 3.1 Geschäftslogik

## 3.2 Benutzeroberfläche (Konsole)

## 3.3 Suche nach Hotels und Zimmern

## 3.4 Verwaltung von Reservierungen

# 4. Datenbankdesign
Das Datenbankdesign für das Hotelreservierungssystem basiert auf einem **Entity-Relationship-Modell** (ER-Modell), 
das die verschiedenen Entitäten und ihre Beziehungen beschreibt. 
Das ER-Modell wurde von den Dozenten bereitgestellt und bildet die Grundlage für die Implementierung des Systems. 
Obwohl wir anfangs Überlegungen angestellt haben, das Modell zur Unterstützung einer dynamischeren Suchfunktion zu verbessern, 
haben wir letztendlich beschlossen, das vorgegebene Modell unverändert zu lassen, um die Einfachheit und Konsistenz zu gewährleisten.
- Beschreibung der Datenbanktabellen und -beziehungen

## 4.1 User Stories
# User Story 3.4: Wir haben uns dafür entschieden eine "availability"-column im model des Rooms hinzuzufügen um die User Story realisieren zu können.
Nun kann ein Hotel-Manager ein Datum ab wann ein Zimmer "unavailable" ist, gleichzeitig löscht das System alle offenen Buchungen (zuerst werden aktive Buchungen in dem Zeitraum noch dem Benutzer angezeigt, bevor man diese Bestätigt zu löschen)
Zudem wird in der Datenbank die Spalte "unavailability_start" und "unavailability_end" gesetzt, denkbar ist dies wenn ein Zimmer ab einem bestimmten Zeitraum für Renovationen nicht mehr verfügbar stehen kann, oder wenn Aufgrund von Schaden od. anderen Gründen das Zimmer nicht zur Verfügung steht.
Diese Datumdefinitionen legen dann fest ab wann neue Buchungen entgegengenommen werden können.

Wichtig anzumerken ist, da diese User Story viele veränderungen mit sich brachte und daher z.B. in dem Reservationsmanager neuen spalten ...start und ...end nicht für die erstellung neuer Buchungen berücksichtigt wurde.
Dies da jeder der Manager von jemand anderem realisiert wurde. Diese implementation zeigt nur wie diese UserStory realisiert werden kann.
- Wir haben zusätzlich zu den User Stories noch die Möglichkeit implementiert Hotelzimmer hinzuzufügen und zu löschen für eine spezifizierte Hotel-ID.
*******- @benz - haben wir noch etwas hinzugefügt das nicht in den user stories steht?

# 5. Anwendung




# 6. Lessons Learned 
- Zusammenfassung der in den Interviews besprochenen Punkte
- Reflexionen der Teammitglieder über das Projekt und die gelernten Konzepte

- Während der Implementierung von UserManager.py fiel auf, dass die User Stories für Gastnutzer und registrierte Benutzer unklar formuliert waren. Um diese Unklarheiten zu beheben, entschieden wir uns, im User-Manager zwei grundlegende Methoden zu verwenden: “create_new_login” für die Erstellung neuer Logins und “register_existing_user” zum Hinzufügen von Benutzerdetails zu einem bestehenden Login.
Nach Rücksprache mit den Coaches stellte sich heraus, dass die User Stories und das Datenbankmodell zu einer grösseren Interpretationsspielraum hatten als bisher angedacht und wir eine alternative Herangehensweise gewählt hatten. Wir behielten den User-Manager mit der erweiterten Funktionalität bei, setzten jedoch die Arbeit am Reservationsmanager gemäss der Vision der Coaches fort.

## 6.1 

## 6.2 Verbesserungsmöglichkeiten
- UserManager.py Subclasses erstellen zur separierung von Gast oder Admin Nutzer (Authentication nicht genau möglich), 
- Wir hatten angenommen, dass ein Benutzer ein Login erstellen kann, unabhängig davon, ob er sich entscheidet, alle Gast Informationen angeben zu müssen. -> "Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können..."
Die Lösung wurde nun so implementiert, dass sich ein Benutzer, der sich unabhängig von einer Buchung registrieren möchte, zunächst nur mit einer E-Mail-Adresse und einem Passwort registrieren kann. Anschliessend kann er in einem zweiten Schritt entscheiden, ob er zusätzliche Gastdetails angeben möchte. 
Diese Interpretation wurde mit Sandro und Charuta besprochen und wurde als alternative Interpretation akzeptiert.
- role_id zuteilung fehlt in register user section 
- nachdem Login sieht man nicht mit welchem user man eingeloggt ist!!!!!!!!!
- room availability komisch verwendet
- HotelManagement wurde nicht optimal implementiert, deshalb konnte das Reservationsmanager nicht 100% funktionieren (get_hotel_id_by_name function fehlt z.B)
- 


# User Story 3.4: 
Hier haben wir angenommen, dass es zur Verwaltung der Zimmerverfügbarkeit erforderlich ist, zusätzliche Spalten im Raummodell zu erstellen.
Wir haben uns entschieden, die Spalten "unavailability_start" und "unavailability_end" im Modell des Rooms hinzuzufügen, um die User Story zu realisieren und zukünftige Anforderungen besser abdecken zu können.
Diese Lösung wurde so implementiert, dass ein Hotelmanager einen Datumsbereich definieren kann, ab wann ein Zimmer nicht verfügbar ("unavailable") ist. Gleichzeitig löscht das System alle offenen Buchungen in diesem Zeitraum. Vor der endgültigen Löschung werden die betroffenen Buchungen dem Benutzer zur Bestätigung angezeigt.
Dies ist nützlich, wenn ein Zimmer ab einem bestimmten Zeitraum für Renovierungen oder aufgrund von Schäden oder anderen Gründen nicht verfügbar ist. Die Spalten "unavailability_start" und "unavailability_end" in der Datenbank legen fest, ab wann keine neuen Buchungen mehr angenommen werden können und ab wann das Zimmer wieder verfügbar ist.
Wichtig zu beachten ist, dass diese User Story viele Änderungen mit sich brachte und daher im Reservationsmanager nicht bei der Erstellung neuer Buchungen berücksichtigt wurde. Aufgrund begrenzter Ressourcen konnten wir die bereits implementierten Funktionen nicht umfassend anpassen.





main.py: Supavadee
UI - MainMenu.py, SearchMenu.py separierung: Supavadee
SearchManager.py: Supavadee
ReservationManager.py: Supavadee, Manuel
console_base.py, HotelManager.py, UserManager.py: Manuel
README.md: Supavadee, Manuel
models.py, data_generator.py: Manuel
Testing Console: Damian

User Stories erarbeitet:
1.-1.5: Supavadee
2.-2.1.1: Supavadee
1.6 + 3.-3.4: Manuel