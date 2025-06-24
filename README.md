# 📊 Election Monitor API – US-Wahlen 2024

A lightweight **FastAPI** application for exploring prediction market data from the **2024 U.S. Presidential and Senate elections**, with focus on key swing states.  
Data is visualized as state-level timelines and a week-by-week heatmap.

---

## 🔎 What This Is

This MVP was built as a public-facing demo based on data components from a confidential project at [DryShaft Data Lab](https://dryshaft.net).  
The original system aggregated data from **Polymarket**, media sources, and NLP pipelines into a multi-screen monitoring dashboard for trading and analytics teams.  
This stripped-down version includes only cleaned prediction market data and public-facing graphs.

🔗 For more background, see the [project description](https://pythia.one/us_wahl_2024.html)  
🌐 **Live demo:** _coming soon_ → `https://your-url-here.com` *(insert after deploy)*

---

## 📦 Project Structure

```
core-utils/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── db/                  # DB models and engine
│   ├── templates/           # Jinja2 HTML pages
│   └── static/              # Style and chart images
│		└──engine.py 		
├── ingest/
│   ├── load_president.py    # Loads CSV → DB
│   ├── load_senate.py
│   ├── generate_all_charts.py
│   └── plot_main_heatmap.py
├── sample_data/
│   └── president_sample.csv, senate/*.csv
├── start.sh                 # Optional bootstrap
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

## ⚠️ Legal / Notes

- The original project is partly covered by an NDA.  
- This repo includes **no confidential code or analysis**.  
- Data was sourced from public market interfaces (Polymarket etc.).  
- Charts are static PNGs generated from anonymized state-level data.

---

🗂️ All credentials are managed via `.env`  
🚫 Do **not** commit `.env`, `.DS_Store`, or `alembic.ini`
