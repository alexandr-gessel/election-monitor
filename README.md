# 📊 Election Predictions API

A **FastAPI** application providing probabilistic predictions for the **2024 U.S. Presidential and Senate elections** by state.  
The data is sourced from CSV files for real-time and historical analysis.

---

## 📦 Project Structure
- `sample_data/`: CSV data for presidential and senate races
- `ingest/loader.py`: data loader module for ingesting CSV files
- `app/`: FastAPI application
    - `models.py`: Pydantic models for data serialization
    - `main.py`: API endpoints for data retrieval

---

## 🚀 How to Run
```bash
uvicorn app.main:app --reload

### 📊 Sample datasets

| File/Folder                           | Format | Rows                   | Notes |
|--------------------------------------|--------|-------------------------|-------|
| `sample_data/president_sample.csv`   | CSV    | All rows from 50 states | Columns: Democratic, Donald Trump, Other |
| `sample_data/senate/` (33 files)     | CSV    | Full volume             | One file per state. Wide format, candidate names vary |
