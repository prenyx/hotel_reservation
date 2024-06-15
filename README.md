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

**Autoren**: *Gruppe B* (Supavadee Theerapong, Manuel Pasamontes, Damian Martin, Steven Chevalley) 

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

### 2.2.3 Testing und Debugging
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

## 3.1 Geschäftslogik
Die Geschäftslogik des Hotelreservierungssystems ist im Ordner `business` implementiert. 
Dieser Ordner enthält mehrere **Manager-Klassen**, die verschiedene Aspekte des Systems verwalten, darunter *Hotels*, *Zimmer*, *Buchungen* und *Benutzer*.

- `HotelManager.py`: Verwalten von Hotel-bezogenen Operationen z.B. Hotels und Räume hinzufügen.
- `ReservationManager.py`: Handhabung von Buchungsprozessen z.B. Reservationen kreieren.  
- `SearchManager.py`: Bereitstellung von Suchfunktionen für Hotels und Zimmer.
- `UserManager.py`: Verwaltung der Benutzerregistrierung und -authentifizierung.

## 3.2 Benutzeroberfläche (Konsole)
Die Benutzeroberfläche des Systems ist als Konsolenanwendung implementiert, die dem Benutzer ermöglicht, verschiedene Funktionen des Systems über Menüs zu bedienen. 
Die Hauptkomponenten der Benutzeroberfläche sind im Ordner console implementiert.

- `console_base.py`: Enthält die Basis-Klassen für die Menüstruktur.
- `mainMenu.py`: Implementiert das Hauptmenü der Anwendung.
- `SearchMenu.py`: Bietet Menüoptionen für die Hotelsuche.
- `ReservationMenu.py`: Bietet Menüoptionen für die Verwaltung von Reservierungen.

## 3.3 Suche nach Hotels und Zimmern
Die Suchfunktionen des Systems sind im SearchManager implementiert, der es ermöglicht, Hotels und Zimmer basierend auf verschiedenen Kriterien zu durchsuchen.

- `search_hotels_by_city`: Sucht Hotels nach Stadt.
- `search_hotels_by_stars`: Sucht Hotels nach Anzahl der Sterne.
- `search_hotels_by_guest_count`: Sucht Hotels nach der maximalen Gästeanzahl.
- `search_hotels_by_date_and_guest_count`: Sucht Hotels nach Verfügbarkeit basierend auf Datum und Gästeanzahl.

## 3.4 Verwaltung von Reservierungen
Die Verwaltung der Reservierungen ist im ReservationManager implementiert. Dieser Manager bietet Funktionen zum Erstellen, Aktualisieren, 
Löschen und Anzeigen von Reservierungen sowie zum Überprüfen der Verfügbarkeit von Zimmern.

- `create_reservation`: Erstellt eine neue Reservierung.
- `update_reservation`: Aktualisiert eine bestehende Reservierung.
- `delete_reservation`: Löscht eine bestehende Reservierung.
- `get_reservation_details`: Ruft die Details einer bestimmten Reservierung ab.
- `list_reservations`: Listet alle Reservierungen auf.
- `check_available_rooms`: Überprüft die Verfügbarkeit von Zimmern in einem bestimmten Zeitraum.

# 4. Datenbankdesign
Das Datenbankdesign für das Hotelreservierungssystem basiert auf einem **Entity-Relationship-Modell** (ER-Modell), 
das die verschiedenen Entitäten und ihre Beziehungen beschreibt. 
Das ER-Modell wurde von den Dozenten bereitgestellt und bildet die Grundlage für die Implementierung des Systems. 
Obwohl wir anfangs Überlegungen angestellt haben, das Modell zur Unterstützung einer dynamischeren Suchfunktion zu verbessern, 
haben wir letztendlich beschlossen, das vorgegebene Modell weitgehend unverändert zu lassen, um die Einfachheit und Konsistenz zu gewährleisten.

## 4.1 Datenbankinitialisierung
Die Initialisierung der Datenbank ist ein entscheidender Schritt zur Bereitstellung der grundlegenden Datenstrukturen und zum Laden von Beispiel- oder Testdaten. 
In diesem Projekt wird die Datenbankinitialisierung durch die Methode `init_db` im Modul `data_base.py` durchgeführt. Diese Methode sorgt dafür, dass alle notwendigen Tabellen erstellt und optional mit Beispiel- oder Testdaten befüllt werden.

**Implementierungsdetails:**

Die Datei `data_base.py` enthält die `init_db`-Funktion, die die Datenbank initialisiert. Diese Funktion übernimmt die folgenden Aufgaben:

- *Datenbankverbindung herstellen*: Stellt eine Verbindung zur SQLite-Datenbank her, die durch den angegebenen Pfad definiert ist.
- *Tabellen erstellen*: Erstellt alle Tabellen, die im Datenmodell definiert sind.
- *Beispieldaten generieren*: Optional können Beispiel- oder Testdaten in die Tabellen eingefügt werden.

**Verwendung der Initialisierungsfunktion:**

Die Datenbankinitialisierung wird in der Datei `main.py` aufgerufen, um sicherzustellen, dass die Datenbank korrekt eingerichtet ist, bevor die Anwendung startet.
## 4.2 User Stories und Datenbankoperationen
Die vorgegebenen User Stories wurden vollständig bearbeitet und weitgehend implementiert. Der größte Teil der User Stories handelt von Gastnutzern, die ein Hotel suchen und reservieren möchten. Dabei wird zwischen registrierten Gästen und Gastnutzern unterschieden. 
Darüber hinaus gibt es noch einen kleinen Abschnitt, der sich mit den Anforderungen der Administratoren befasst.

**User Story: 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen.**

*Datenbankoperation*: Implementierung der Suchfunktion in SearchManager, die Hotels nach Stadt durchsucht.
- `search_hotels_by_city`

**User Story: 3.4. Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und
die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren
(Optional).**

Um diese User Story zu realisieren, wurde eine availability-Spalte im Room-Modell hinzugefügt, leider ohne Absprache mit den Dozenten. 

Nun kann ein Hotel-Manager ein Datum angeben, ab wann ein Zimmer "unavailable" ist. 
Gleichzeitig löscht das System alle offenen Buchungen (zuerst werden aktive Buchungen in dem Zeitraum dem Benutzer angezeigt, 
bevor man diese bestätigt zu löschen). Zudem werden in der Datenbank die Spalten unavailability_start und unavailability_end gesetzt. 
Dies ist beispielsweise nützlich, wenn ein Zimmer in einem bestimmten Zeitraum für Renovationen nicht mehr verfügbar ist oder aus anderen Gründen nicht zur Verfügung steht. 
Diese Datum definitionen legen dann fest, ab wann neue Buchungen entgegengenommen werden können.

*Datenbankoperation*: Implementierung der Verfügbarkeitscheck-Funktion im ReservationManager, die nach verfügbaren Räumen sucht.

# 5. Anwendung
Die Anwendung des Hotelreservierungssystems wurde in mehrere Module unterteilt, die jeweils spezifische Funktionen zur Verwaltung von Hotels, Zimmern, Buchungen und Benutzern bieten. 
Die Anwendung ist in Python implementiert und nutzt die SQLAlchemy-Bibliothek zur Datenbankverwaltung.

Um die Applikation zu starten, muss lediglich die `main.py`-Datei ausgeführt werden. 
Bei der erstmaligen Nutzung wird automatisch ein Superuser erstellt.
Das Benutzerinterface wurde im ui-Ordner implementiert.

## 5.1 Hauptmenü und Navigation
Das Hauptmenü der Anwendung dient als zentrale Anlaufstelle für den Benutzer. 
Hier können verschiedene Aktionen ausgewählt werden, wie z.B. das Durchsuchen von Hotels, die Verwaltung von Buchungen oder die Benutzerregistrierung. 
Die Navigation durch die Menüs wird über das `console_base.py`-Modul gesteuert.

# 6. Lessons Learned 

Zu Beginn des Projekts hatte die Gruppe keine klare Vorstellung davon, wie die endgültige Applikation aussehen sollte. 
Deshalb wurden zunächst die User Stories implementiert. Auch die Implementierung der Benutzeroberfläche (UI) war unklar, da die Gruppe anfangs davon ausging, eine Web-Applikation zu entwickeln. 
Daher konnte die Strukturierung der einzelnen Dateien und die Erstellung von Sub-Klassen nicht genau abgestimmt werden.

Wegen dieser Unklarheiten in der Anfangsphase konnte die Gruppe leider nicht genau entscheiden, wie die Klassen im business-Ordner definiert werden sollten. 
Erst in der Schlussphase des Projekts wurde deutlicher, wie die gesamte Applikation aussehen sollte. 
Letztendlich wurde für die Benutzeroberfläche ein Terminal-Interface implementiert.

Daraus konnte die Gruppe lernen, dass es essenziell ist, eine klare Vorstellung und detaillierte Planung zu Beginn des Projekts zu haben, 
um Missverständnisse und Unklarheiten zu vermeiden. Somit kann die erfolgreiche Implementierung der Applikation sichergestellt werden.

Das Team lernte auch, flexibel zu sein und sich an unerwartete Änderungen anzupassen. 
Es zeigte sich, wie wichtig es ist, offen für neue Ansätze zu sein, wenn die ursprünglichen Annahmen nicht realisierbar sind.

**Supavadee:**

Durch die Bearbeitung des Projekts konnte ich meine theoretischen Kenntnisse von Datenbanken in die Praxis umsetzen. 
Zudem habe ich gelernt, wie man eine Datenbank von Grund auf implementiert. 
Mein Wissen zur Implementierung von Benutzeroberflächen (UI) wurde ebenfalls vertieft und erweitert.
Beispielsweise habe ich jetzt ein besseres Verständnis für die Implementierung der Navigationsfunktion "Zurück" sowie dafür, 
wie man eine Datenbank initialisiert.

**Manuel:**

Während der Implementierung von User Stories für den UserManager fiel mir auf, dass die User Stories für Gastnutzer und registrierte Benutzer unklar formuliert waren. Um Unklarheiten zu beheben, 
entschied ich mich, in der UserManager-Datei zwei grundlegende Methoden zu verwenden: `create_new_login` zur Erstellung neuer Logins und `register_existing_user` zum Hinzufügen von Benutzerdetails zu einem bestehenden Login.

Nach Rücksprache mit den Coaches stellte sich heraus, dass die User Stories und das Datenbankmodell einen größeren Interpretationsspielraum hatten als ursprünglich gedacht 
und ich eine alternative Herangehensweise gewählt hatte. Ich behielt den UserManager mit der erweiterten Funktionalität bei, setzte jedoch die Arbeit am ReservationManager gemäß der Vision der Coaches fort.

Ich hatte angenommen, dass ein Benutzer ein Login erstellen kann, unabhängig davon, ob er sich entscheidet, alle Gastinformationen anzugeben. 
Dies entsprach der User Story: "Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können..."

Die Lösung wurde nun so implementiert, dass sich ein Benutzer, der sich unabhängig von einer Buchung registrieren möchte, 
zunächst nur mit einer E-Mail-Adresse und einem Passwort registrieren kann. Anschließend kann er in einem zweiten Schritt entscheiden, 
ob er zusätzliche Gastdetails angeben möchte. Diese Interpretation wurde mit Sandro und Charuta besprochen und als alternative Interpretation akzeptiert.

**Damian:**
Während der Entwicklung habe ich erlebt, wie wichtig es ist, klare Absprachen zu treffen und sich frühzeitig über die Anforderungen im Klaren zu sein. Unser Team musste die ursprüngliche Planung überarbeiten, 
da es Missverständnisse gab, die aus unklaren Anforderungen resultierten. Wir stießen auf unerwartete technische Herausforderungen, 
die eine Anpassung unserer Strategie erforderten. Durch die Anwendung agiler Methoden konnten wir schnell reagieren und Lösungen finden, 
die besser zu den neuen Anforderungen passten. Insgesamt hat dieses Projekt mein Verständnis für die Bedeutung einer strukturierten Herangehensweise gestärkt.

**Steven:**
Während des Projekts konnte ich anfangs nicht aktiv mitarbeiten, da mein Wissen nicht auf dem gleichen Stand wie das meiner Teammitglieder war. Um die notwendigen Kenntnisse zu erwerben, musste ich mich zuerst intensiv mit Python auseinandersetzen.
Glücklicherweise standen mir die anderen Mitglieder der Gruppe immer zur Seite. Bei Fragen oder Problemen boten sie mir stets wertvolle Unterstützung an. Geduldig erklärten sie mir, wie das Projekt zustande kam und welche Schritte notwendig waren, um die Aufgaben zu bewältigen.
Durch ihre Hilfe konnte ich mein Wissen über Python erheblich erweitern. Mit der Zeit entwickelte sich mein Verständnis für die Programmiersprache, und ich begann, zunehmend Freude an der Arbeit zu finden. Diese Erfahrung half mir nicht nur, mein technisches Know-how zu verbessern, sondern stärkte auch mein Selbstvertrauen im Umgang mit neuen Herausforderungen.
Ich erkannte auch, dass ein Team sich gegenseitig unterstützen kann, selbst wenn die Wissensniveaus unterschiedlich sind. Diese Zusammenarbeit und Unterstützung im Team waren entscheidend dafür, dass ich mich weiterentwickeln konnte und das Projekt erfolgreich vorangetrieben wurde.

## 6.2 Teamkoordination und Kommunikation
Die Gruppe hat sich für eine Rollenzuteilung entschieden, die zwei Rollen umfasste: Entwickler und Tester. 
Das Entwicklerteam bestand aus Manuel Pasamontes und Supavadee Theerapong. Die Tester, Damian Martin und Steven Chevalley, haben am Schluss die Applikation getestet.

Jeden Montag wurde ein kurzes Gruppenmeeting durchgeführt, um zu besprechen, was bis zur nächsten Woche erledigt werden soll. 
Durch bessere Koordination hätten jedoch Missverständnisse und Verzögerungen vermieden werden können. Dies hätte beispielsweise durch detailliertere Aufgabenverteilung, 
klarere Zielsetzungen und häufigerem Austausch über den Fortschritt der einzelnen Teammitglieder erreicht werden können.



## 6.3 Verbesserungsmöglichkeiten
- UserManager.py Subclasses erstellen zur separierung von Gast oder Admin Nutzer (Authentication nicht genau möglich), 
- Wir hatten angenommen, dass ein Benutzer ein Login erstellen kann, unabhängig davon, ob er sich entscheidet, alle Gast Informationen angeben zu müssen. -> "Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können..."
Die Lösung wurde nun so implementiert, dass sich ein Benutzer, der sich unabhängig von einer Buchung registrieren möchte, zunächst nur mit einer E-Mail-Adresse und einem Passwort registrieren kann. Anschliessend kann er in einem zweiten Schritt entscheiden, ob er zusätzliche Gastdetails angeben möchte. 
Diese Interpretation wurde mit Sandro und Charuta besprochen und wurde als alternative Interpretation akzeptiert.
- role_id zuteilung fehlt in register user section (wäre separate user story)
- nachdem Login sieht man nicht mit welchem user man eingeloggt ist!!!!!!!!! -> was bedeutet das, welcher login/wo
- room availability komisch verwendet -> was bedeutet das
- HotelManagement wurde nicht optimal implementiert, deshalb konnte das Reservationsmanager nicht 100% funktionieren (get_hotel_id_by_name function fehlt z.B) -> wie hätte man es "optimal" implementiert?
- Password hashing sowie auch non-cleartext passwort eingabe zumindest.
- 

# 7. Fazit


main.py: Supavadee
UI - MainMenu.py, SearchMenu.py separierung: Supavadee
SearchManager.py: Supavadee
ReservationManager.py: Supavadee, Manuel
console_base.py, HotelManager.py, UserManager.py: Manuel
README.md: Supavadee, Manuel
models.py, data_generator.py: Manuel
Testing Console: Damian

User Stories erarbeitet:
1.-1.5 + 2.-2.1.1: Supavadee
1.6 + 3.-3.4: Manuel