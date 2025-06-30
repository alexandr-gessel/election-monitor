# 📊 Election Monitor API – US-Wahlen 2024  
**FastAPI-based site with static visualizations for U.S. Election Predictions**

Eine leichtgewichtige **FastAPI-Anwendung** zur Darstellung von Prognosedaten aus Vorhersagemärkten zur **US-Präsidentschafts- und Senatswahl 2024**, mit Fokus auf zentrale „Swing States“.  
Die Daten werden als Zeitreihen auf Bundesstaatenebene und als Heatmap nach Kalenderwochen visualisiert.

---

## 🔎 Was ist das?

Dieses MVP wurde als öffentlich zugängliches Demoprojekt entwickelt und basiert auf Datenmodulen eines vertraulichen Projekts bei [DryShaft Data Lab](https://dryshaft.net).  
Das ursprüngliche System aggregierte Informationen aus **Polymarket**, Medienquellen und NLP-Pipelines in einem Multi-Screen-Dashboard zur Echtzeit-Überwachung für Analyse- und Trading-Teams.  
Die hier gezeigte reduzierte Version enthält ausschließlich bereinigte Prognosedaten und öffentlich darstellbare Grafiken.

🔗 Weitere Hintergründe: [Projektbeschreibung](https://pythia.one/us_wahl_2024.html)  
🌐 **Live-Demo:** [https://election-monitor.up.railway.app](https://election-monitor.up.railway.app)

---

## 🧾 Hinweis zur Datenbank

Ursprünglich wurde die API mit einer vollständigen PostgreSQL-Datenbank, Alembic und SQLAlchemy betrieben, 
um Prognosedaten zu erfassen und zu aggregieren. Nach mehreren Iterationen mit HTML-Templates und Visualisierungen 
wurde die Datenbank jedoch aus dem Deployment entfernt.

Das Projekt läuft nun **ohne aktive Datenbank** – alle Diagramme wurden einmalig manuell generiert und als PNG gespeichert.  
FastAPI wird weiterhin in einem Docker-Container (über Railway) ausgeführt, verarbeitet jedoch keine Datenbankabfragen mehr.  
Die Abhängigkeiten von Alembic, SQLAlchemy und asyncpg sind noch vorhanden, werden jedoch nicht mehr verwendet.


---

## 📦 Project Structure

```
core-utils/
├── app/
│   ├── main.py              # FastAPI-Einstiegspunkt
│   ├── db/                  # Datenbankmodelle und Engine (nicht aktiv)
│   ├── templates/           # Jinja2 HTML pages
│   └── static/              # Style and chart images
│		└──engine.py 		
├── ingest/
│   ├── load_president.py    # Loads CSV → DB
│   ├── load_senate.py       # Loads JSON → DB
│   ├── generate_all_charts.py
│   └── plot_main_heatmap.py
├── sample_data/
│   └── president_sample.csv, senate_combined.json
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🚀 How to Run (Docker)

```bash
# 1. Clone and prepare .env
cp .env.example .env

# 2. Start PostgreSQL and API
docker-compose up --build

# 3. Apply migrations inside the container
docker exec -it election-api bash
alembic upgrade head
```

(Optional) Load data and generate charts:
```bash
PYTHONPATH=. python ingest/load_president.py
PYTHONPATH=. python ingest/load_senate.py
PYTHONPATH=. python ingest/generate_all_charts.py
```

---

## 🔌 API Endpoints

### Presidential race
- `GET /president/{state}` – all records for state
- `POST /president/` – add prediction

### Senate race
- `GET /senate/{state}` – all records for state
- `POST /senate/` – add prediction

---

## 🌐 Frontend (Jinja2)

- `/` — overview with heatmap and categorized states
- `/state/{state}` — detailed charts for one state
- `/about.html` — context and origin of data

---

## 🛠 Tech Stack

- **FastAPI** / **Jinja2** / **Tailwind CSS**
- **PostgreSQL** / **SQLAlchemy 2.0** / **Asyncpg**
- **matplotlib** / **seaborn** / **pandas**
- **Docker Compose**

---

## ⚠️ Rechtlicher Hinweis

- Das ursprüngliche Projekt unterliegt teilweise einer **Geheimhaltungsvereinbarung (NDA)**.  
- Dieses Repository enthält **keinen vertraulichen Code oder Analysen**.  
- Die verwendeten Daten stammen ausschließlich aus öffentlich zugänglichen Vorhersagemärkten (z. B. Polymarket).  
- Alle Diagramme wurden auf Basis **anonymisierter und bereinigter State-Level-Daten** als PNG-Dateien generiert.

---

🗂️ Alle Zugangsdaten und Konfigurationswerte werden über `.env` verwaltet.  
🚫 Dateien wie `.env`, `.DS_Store` oder `alembic.ini` sollten **nicht** eingecheckt werden.
