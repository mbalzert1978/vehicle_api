# vehicle_api

create a .env file like this:

```.env
APP_ENV=dev
DEBUG=True
DATABASE_URL=postgresql://user:pw@127.0.0.1/table
```

have a db running like this:

### Postgres Schema

```sql
CREATE TABLE vehicle (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	year_of_manufacture INTEGER NOT NULL,
	body JSON NOT NULL,
	ready_to_drive BOOLEAN NOT NULL,
	PRIMARY KEY (id)
)
```

or just create a new database named db or whatever you name it in the .env file.

Then run :

```bash
poetry run alembic upgrade head
```

## Webanwendung:

- Quellcode in einem zugänglichen Git-Repo (entweder öffentlich zugänglich oder mit spezieller Einladung)
- vorzugsweise nicht nur ein einziger Commit, sondern mit etwas Historie, um eine Vorstellung davon zu bekommen, wie Sie diese Herausforderung angegangen sind
- FastAPI Webanwendung (json API)
- PostgreSQL-Datenbank für die Speicherung der Daten
- wir würden gerne vier Endpunkte sehen: - einen Status-Endpunkt zur Überprüfung des Dienstzustandes - einen Endpunkt für das Hinzufügen eines Datensatzes zur Datenbank - ein Endpunkt zum Abrufen aller Datensätze aus der Datenbank (keine Paginierung erforderlich) - der letzte Endpunkt wäre für die Aktualisierung eines bestehenden Datensatzes
- Unser Vorschlag für die zu speichernden Daten wäre:
  "vehicle"-Datensätze mit einigen verschiedenen Datentypen. z.B.:
  "name" (Freitext)
  "metadata" (JSON-Daten)
  "year_of_manufacture" (Ganzzahl)
  "ready_to_drive" (Boolean)
- eine swagger-ui, die möglichst aussagekräftig ist (Auskunft über erwartete Eingabeparameter und zu erwartende Responses, Beispiele, Defaults).

Optional, aber nicht zwingend erforderlich:

- eine Möglichkeit eine Teilmenge von Datensätzen abzurufen (z.B. eine einfache Art Suche oder Filterung)

### NICHT ERFORDERLICH: HTML, CSS, Authentifizierung/Authorisierug, Deployment, DB-Migrationen, Unittests, Docker-Setup. Für die Datenbank reicht uns das Schema als SQL-Datei.
