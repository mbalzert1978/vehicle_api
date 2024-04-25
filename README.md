# vehicle_api

create a .env file like this:

```.env
DATABASE_URL=postgresql+asyncpg://app:app@app_db:5432/app

SITE_DOMAIN=127.0.0.1

ENVIRONMENT=LOCAL

CORS_HEADERS=["*"]
CORS_METHODS=["*"]
CORS_ORIGINS=["http://localhost:3000"]

API_PREFIX="/api/v1"


# postgres variables, must be the same as in DATABASE_URL
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_HOST=app_db
POSTGRES_PORT=5432
POSTGRES_DB=app
```

have a db running like this:

### Postgres Schema

```sql
CREATE TABLE vehicles (
	id CHAR(32) NOT NULL,
	name VARCHAR NOT NULL,
	manufacturing_year INTEGER NOT NULL,
	is_driveable BOOLEAN,
	body JSON,
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	updated_at DATETIME,
	CONSTRAINT vehicles_pkey PRIMARY KEY (id)
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
