# ingest/generate_all_charts.py

import asyncio
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import select
from app.db.engine import get_session
from app.db.session import PresidentPredictionDB, SenatePredictionDB

OUTPUT_DIR = "app/static/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def fetch_president_data():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        result = await session.execute(select(PresidentPredictionDB))
        records = result.scalars().all()
        return [r.__dict__ for r in records]
    finally:
        await session_gen.aclose()

async def fetch_senate_data():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        result = await session.execute(select(SenatePredictionDB))
        records = result.scalars().all()
        return [r.__dict__ for r in records]
    finally:
        await session_gen.aclose()

def plot_president_by_state(df, state):
    df_state = df[df['state'] == state].copy()
    df_state = df_state.sort_values(by='date')

    if df_state.empty:
        return

    plt.figure(figsize=(20, 8))
    plt.plot(df_state['date'], df_state['trump'], marker='o', label="Donald Trump", color='#dc2626')
    plt.plot(df_state['date'], df_state['democratic'], marker='o', label="Kamala Harris", color='#1d4ed8')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{state}_president.png")
    plt.close()

def plot_senate_by_state(df, state):
    df_state = df[df['state'] == state].copy()
    df_state = df_state.sort_values(by='date')

    if df_state.empty:
        return

    plt.figure(figsize=(20, 8))
    plt.plot(df_state['date'], df_state['candidate_1'], marker='o', label=df_state['candidate_1_name'].iloc[0], color='#1e40af')
    plt.plot(df_state['date'], df_state['candidate_2'], marker='o', label=df_state['candidate_2_name'].iloc[0], color='#b91c1c')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{state}_senate.png")
    plt.close()

async def main():
    pres_data = await fetch_president_data()
    sen_data = await fetch_senate_data()

    df_pres = pd.DataFrame(pres_data)
    df_pres['date'] = pd.to_datetime(df_pres['date'])
    states_pres = df_pres['state'].unique()

    df_sen = pd.DataFrame(sen_data)
    df_sen['date'] = pd.to_datetime(df_sen['date'])
    df_sen['week'] = df_sen['date'].dt.to_period("W").apply(lambda r: r.start_time)

    agg = df_sen.groupby(['state', 'week']).agg({
        'candidate_1': 'mean',
        'candidate_2': 'mean',
        'candidate_1_name': 'first',
        'candidate_2_name': 'first'
    }).reset_index()
    agg = agg.rename(columns={'week': 'date'})

    states_sen = agg['state'].unique()

    for state in states_pres:
        plot_president_by_state(df_pres, state)
        print(f"✓ saved {state}_president.png")

    for state in states_sen:
        plot_senate_by_state(agg, state)
        print(f"✓ saved {state}_senate.png")

if __name__ == "__main__":
    asyncio.run(main())
