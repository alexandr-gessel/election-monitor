#!/bin/bash

# warte DB ab
echo "⏳ Waiting for PostgreSQL..."
sleep 5

# bildchen
echo "📊 Generating main heatmap..."
PYTHONPATH=. python ingest/plot_main_heatmap.py

echo "📊 Generating all state charts..."
PYTHONPATH=. python ingest/generate_all_charts.py

# FastAPI
echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000