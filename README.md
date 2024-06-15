---
Business_Name:Business Artificial IntelligenceModule_Info:   
Name: Anwendungsentwicklung mit Python  
Authors:        
  - Supavadee Theerapong    
  - Manuel Pasamontes    
  - Damian Martin    
  - Steven Chevalley
Roles:
  - Developers: Supavadee Theerapong, Manuel Pasamontes
  - Tester: Damian Martin, Steven Chevalley 
---
---
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
   - *Beschreibung*: Verwaltung von Hotelinformationen und Zimmerdetails, einschliesslich Verfügbarkeit und spezifischen Zimmermerkmalen.
   - *Entitäten*:
     - Hotel: Informationen zu Hotels, einschliesslich Name, Sternebewertung und Adresse.
     - Room: Details zu den Zimmern, einschliesslich Zimmernummer, Typ, Preis und Verfügbarkeit.

4. **Buchungsverwaltung**:
   - *Beschreibung*: Dieses Modul kümmert sich um die Verwaltung von Zimmerbuchungen, einschliesslich der Verknüpfung von 
   Gästen und Zimmern sowie der Buchungsdetails.
   - *Entitäten*: 
     - Booking: Speichert Informationen zu Buchungen, einschliesslich Datum, 
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
Die vorgegebenen User Stories wurden vollständig bearbeitet und weitgehend implementiert. Der grösste Teil der User Stories handelt von Gastnutzern, die ein Hotel suchen und reservieren möchten. Dabei wird zwischen registrierten Gästen und Gastnutzern unterschieden. 
Darüber hinaus gibt es noch einen kleinen Abschnitt, der sich mit den Anforderungen der Administratoren befasst.

**User Story: 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen.**

*Datenbankoperation*: Implementierung der Suchfunktion in SearchManager, die Hotels nach Stadt durchsucht.
- `search_hotels_by_city`

**User Story: 3.4. Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und
die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren
(Optional).**

Um diese User Story zu realisieren, wurde eine availability-Spalte im Room-Modell hinzugefügt, leider ohne Absprache mit den Dozenten. 

Ein Hotelmanager kann nun ein Datum festlegen, ab dem ein Zimmer als "nicht verfügbar" markiert wird. Das System überprüft gleichzeitig, ob es bestehende Buchungen in diesem Zeitraum gibt. 
Diese offenen Buchungen werden dem Hotelmanager angezeigt, der dann entscheiden kann, ob er diese Buchungen automatisch durch das System stornieren lassen möchte.

In der Datenbank werden die Spalten "unavailability_start" und "unavailability_end" entsprechend aktualisiert. 
Dies ist besonders nützlich, wenn ein Zimmer beispielsweise für Renovierungsarbeiten oder aus anderen Gründen in einem bestimmten Zeitraum nicht verfügbar ist. 
Diese Zeitspanne bestimmt dann, ab wann wieder neue Buchungen für das Zimmer entgegengenommen werden können.

*Datenbankoperation*: Implementierung der Verfügbarkeitscheck-Funktion im ReservationManager, die nach verfügbaren Räumen sucht.

# 5. Anwendung
Die Anwendung des Hotelreservierungssystems wurde in mehrere Module unterteilt, die jeweils spezifische Funktionen zur Verwaltung von Hotels, Zimmern, Buchungen und Benutzern bieten. 
Die Anwendung ist in Python implementiert und nutzt die SQLAlchemy-Bibliothek zur Datenbankverwaltung.

Um die Applikation zu starten, muss lediglich die `main.py`-Datei ausgeführt werden. 
Bei der erstmaligen Nutzung wird automatisch ein Superuser erstellt.
Das Benutzerinterface wurde im ui-Ordner implementiert.

Beim Start der Applikation überprüft das System, ob bereits Daten in der Datenbank vorhanden sind. Falls keine Daten gefunden werden, werden automatisch Beispiel-Daten generiert, 
um eine initiale Datenbasis bereitzustellen. Dies umfasst die Erstellung von Hotels, Gästen, Buchungen und weiteren notwendigen Datensätzen.

## 5.1 Hauptmenü und Navigation
Das Hauptmenü der Anwendung dient als zentrale Anlaufstelle für den Benutzer. 
Hier können verschiedene Aktionen ausgewählt werden, wie z.B. das Durchsuchen von Hotels, die Verwaltung von Buchungen oder die Benutzerregistrierung. 
Die Navigation durch die Menüs wird über das `console_base.py`-Modul gesteuert.

Die Implementierung für das Hauptmenü wurde im `mainMenu.py` codiert. Die Auswahlmöglichkeiten für die Hauptnavigation bestehen aus:
1. Hotels suchen und Anschauen
2. Buchungsmenü
3. Login für Admin
4. Hotelmanagement
5. Beenden


Ursprünglich war geplant, das Hotelmanagement-Menü erst nach einem erfolgreichen Admin-Login anzuzeigen. Aufgrund von Zeitmangel 
und zur Vereinfachung wird dieses Menü jedoch bereits im Hauptmenü angezeigt. 

Zusätzlich sollte nach der Auswahl des Buchungsmenüs eigentlich eine weitere Auswahlseite erscheinen, auf der der Nutzer wählen kann, 
ob er Buchungen als Gastnutzer oder als registrierter Nutzer tätigen möchte. Falls es sich um einen registrierten Nutzer handelt, sollten anschließend Optionen wie "Update Reservation", "View All Reservations" usw. angezeigt werden.

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

Nach Rücksprache mit den Coaches stellte sich heraus, dass die User Stories und das Datenbankmodell einen grösseren Interpretationsspielraum hatten als ursprünglich gedacht 
und ich eine alternative Herangehensweise gewählt hatte. Ich behielt den UserManager mit der erweiterten Funktionalität bei, setzte jedoch die Arbeit am ReservationManager gemäss der Vision der Coaches fort.

Ich hatte angenommen, dass ein Benutzer ein Login erstellen kann, unabhängig davon, ob er sich entscheidet, alle Gastinformationen anzugeben. 
Dies entsprach der User Story: "Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können..."

Die Lösung wurde nun so implementiert, dass sich ein Benutzer, der sich unabhängig von einer Buchung registrieren möchte, 
zunächst nur mit einer E-Mail-Adresse und einem Passwort registrieren kann. Anschliessend kann er in einem zweiten Schritt entscheiden, 
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
Das Entwicklerteam bestand aus Manuel Pasamontes und Supavadee Theerapong, während die Tester, Damian Martin und Steven Chevalley, am Ende die Applikation getestet haben.

Jeden Montag wurde ein kurzes Gruppenmeeting durchgeführt, um zu besprechen, was bis zur nächsten Woche erledigt werden soll. 
Durch bessere Koordination hätten jedoch Missverständnisse und Verzögerungen vermieden werden können. Dies hätte beispielsweise durch detailliertere Aufgabenverteilung, 
klarere Zielsetzungen und häufigeren Austausch über den Fortschritt der einzelnen Teammitglieder erreicht werden können.

Das Kommunikationsprotokoll im Kanban-Board wurde nur gelegentlich aktualisiert, und leider führten einige Mitglieder keine regelmässigen Statusupdates durch.

*User Stories erarbeitet:*
- Supavadee: 1.-1.5 + 2.-2.1.1
- Manuel: 1.6 + 3.-3.4

## 6.3 Verbesserungsmöglichkeiten
- **Subclasses im UserManager.py:** Es wäre sinnvoll, Subklassen für Gast- und Admin-Nutzer zu erstellen, 
um die Authentifizierung und Verwaltung der verschiedenen Nutzerrollen zu erleichtern.

- **Login-Anzeige:** Nach dem Login sieht man nicht, mit welchem Benutzer man eingeloggt ist. Dies führt zu Verwirrung darüber, 
welcher Benutzer aktuell angemeldet ist und sollte daher klar angezeigt werden.

- **Zimmerverfügbarkeit:** Die aktuelle Implementierung der Zimmerverfügbarkeit weist mehrere Mängel auf. 
Die Verfügbarkeit der Zimmer wurde direkt durch Änderungen der `unavailability_start` und `unavailability_end` Daten manipuliert, 
ohne sicherzustellen, dass diese Änderungen in anderen Buchungen oder Teilen der Applikation korrekt reflektiert werden. Es gibt keine Überprüfung, 
ob die angegebenen Daten sich mit bestehenden Buchungen oder anderen Unverfügbarkeiten überschneiden, was zu Inkonsistenzen führen kann. 
Zudem fehlt eine klare Rückmeldung an den Benutzer, ob die Änderungen erfolgreich waren oder ob Fehler aufgetreten sind. 
Eine optimale Implementierung sollte die Verfügbarkeit der Zimmer bei jeder Buchung und jedem Zugriff auf die Verfügbarkeit synchronisieren, Überschneidungen vermeiden, Transaktionen und Sperrmechanismen verwenden und dem Benutzer klare Bestätigungen und Fehlermeldungen zurückgeben.

- **Optimierung des HotelManagements:** Die derzeitige Implementierung des *HotelManagements* weist mehrere Schwächen auf, 
die die vollständige Funktionsfähigkeit des *ReservationsManagers* beeinträchtigen. Um die Effizienz und Benutzerfreundlichkeit zu steigern, 
wurde die Methode `get_hotel_id_by_name` zusätzlich in den *ReservationsManager* integriert. Diese Methode ermöglicht eine gezielte Abfrage der Hotel-ID anhand des Hotelnamens, 
was die Implementierung deutlich effizienter gestaltet.
Am besten wäre es gewesen, einen "Service-Layer" einzurichten, der allgemeine Funktionen wie `get_hotel_id_by_name` bereitstellt und sowohl vom *HotelManagement* als auch vom *ReservationsManager* genutzt wird. 
Auf diese Weise könnten alle häufig genutzten Methoden zur Verwaltung von Hotelinformationen zentral platziert werden.
Zusätzlich wäre die Erstellung einer gemeinsamen abstrakten Basisklasse für alle Manager (z.B. *HotelManagement*, *ReservationsManager*) sinnvoll. 
Beide Manager könnten diese Basisklasse erben und somit Zugriff auf diese Methode haben.

- **Passwortsicherheit:** Sicherheit hat oberste Priorität, insbesondere wenn es um Benutzerdaten geht. 
Die aktuelle Implementierung der Passwortspeicherung ist unzureichend, da Passwörter momentan im Klartext gespeichert werden und kein Passwort-Hashing umgesetzt wurde. 
Es wäre vorteilhaft gewesen, wenn in der Vorlesung zusätzlich das Konzept des Passwort-Hashings behandelt worden wäre.

- **SerchManager - Session:** Derzeit funktioniert die Session-Verbindung im SearchManager nicht richtig. Im Buchungsmenü kann zwar navigiert werden, aber sobald eine Option ausgewählt wird, 
kehrt die Verbindung direkt zum Hauptmenü zurück. Aufgrund von Zeitmangel konnte dieser Fehler leider nicht behoben werden.

# 7. Fazit

Das Projekt war eine spannende Gelegenheit, zu erleben, wie ein Programmierungsprojekt im Team funktioniert. 
Neben den technischen Fähigkeiten haben die Studierenden auch wertvolle Erfahrungen in der Teamarbeit und Kommunikation gesammelt. 
Ein wichtiger Aspekt des Projekts war die Nutzung von Git/GitHub, wodurch die Studierenden lernten, wie man effektiv Versionskontrollsysteme verwendet.

Die Dozenten gaben den Studierenden viel Freiraum in der Implementierung, 
was den Lernprozess förderte und es den Studierenden ermöglichte, ihre Kreativität und Problemlösungsfähigkeiten zu entfalten. 
Dieser Ansatz half den Studierenden, das Programmieren auf eine praxisnahe Weise zu erlernen.

Unser Projekt war komplexer als ursprünglich geplant, da einige Gruppenmitglieder bereits über einige Programmiererfahrungen verfügten. 
Dies führte zu einer anspruchsvolleren Implementierung, von der alle Teammitglieder profitieren konnten, indem sie ihre Fähigkeiten erweiterten und voneinander lernten.

Insgesamt war das Projekt eine bereichernde Erfahrung, die nicht nur technische Fertigkeiten, sondern auch die Bedeutung von Teamarbeit und effektiver Kommunikation in der Softwareentwicklung verdeutlichte.
