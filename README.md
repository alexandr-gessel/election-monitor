# 📊 Election Predictions API

A **FastAPI** application providing probabilistic forecasts for the **2024 U.S. Presidential and Senate elections**, by state.  
The data is sourced from real-time and historical snapshots collected from **Polymarket**, processed and served via API.

---

## 📦 Project Structure

- **`sample_data/`**  
  Contains CSV files with probabilistic predictions:

  | File/Folder                         | Format | Description |
  |-------------------------------------|--------|-------------|
  | `president_sample.csv`              | CSV    | All states, 2024 Presidential race |
  | `senate/` (33 files)                | CSV    | One file per state; Senate races, candidates vary |

- **`ingest/`**  
  Data ingestion scripts:
  - `loader.py`: in-memory loader for CSVs
  - `load_president.py`: Loads `president_sample.csv` into the database
  - `load_senate.py`: Loads 33 Senate CSVs into the database

- **`app/`**  
  FastAPI backend code:
  - `models.py`: Pydantic request models
  - `main.py`: API routes
  - `db/session.py`: SQLAlchemy models
  - `db/engine.py`: Async DB engine

---

## 🚀 How to Run

1. Create `.env` in the root:

   ```bash
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost/election
   ```

2. Apply migrations:

   ```bash
   alembic upgrade head
   ```

3. Start the server:

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🔌 API Endpoints

### ✅ President Race

- `GET /president/{state}`  
  → Returns all records for the given state

- `POST /president/`  
  → Adds a new prediction to the database

### ✅ Senate Race

- `GET /senate/{state}`  
  → Returns all records for the given state

- `POST /senate/`  
  → Adds a new prediction to the database

---

## 🛠 Tech Stack

- **FastAPI** — backend framework
- **SQLAlchemy 2.0 + AsyncSession** — ORM
- **Alembic** — DB migrations
- **PostgreSQL** — database
- **Pydantic** — validation and typing

---

## 🧪 Test & Future

This project is an early MVP for election prediction analysis.  
Further development may include:
- Frontend interface for exploring states
- Graphs for prediction timelines
- Deployment to a public server

---

📂 All credentials and secrets are managed via `.env`  
🛑 Do **not** commit `alembic.ini`, `.env`, or `.DS_Store`
