# ingest/plot_main_heatmap.py

import asyncio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from sqlalchemy import select
from app.db.engine import get_session
from app.db.session import PresidentPredictionDB

OUTPUT_PATH = "app/static/charts/main.png"
SWING_AND_KEY_STATES = {
    'MI': 'Michigan',
    'NV': 'Nevada',
    'PA': 'Pennsylvania',
    'WI': 'Wisconsin',
    'CA': 'California',
    'TX': 'Texas',
    'GA': 'Georgia',
    'AZ': 'Arizona'
}

async def fetch_data():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        result = await session.execute(select(PresidentPredictionDB))
        records = result.scalars().all()
        return [r.__dict__ for r in records if r.state in SWING_AND_KEY_STATES]
    finally:
        await session_gen.aclose()

def preprocess(df_raw):
    df = pd.DataFrame(df_raw)
    df = df[['state', 'date', 'democratic', 'trump']]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df['delta'] = df['trump'] - df['democratic']
    df['week'] = df['date'].dt.to_period("W").apply(lambda r: r.start_time)

    grouped = df.drop_duplicates(subset=['state', 'week'])[['state', 'week', 'delta']]
    pivot = grouped.pivot(index='state', columns='week', values='delta')

    if pivot.shape[1] != 32:
        print(f"Warning: got {pivot.shape[1]} weeks instead of 32")

    pivot = pivot.fillna(0)
    return pivot

def plot_heatmap(data):
    plt.figure(figsize=(14, 6))
    norm = TwoSlopeNorm(vmin=-3, vcenter=0, vmax=3)
    cmap = sns.diverging_palette(250, 10, as_cmap=True)

    sns.heatmap(
        data,
        cmap=cmap,
        norm=norm,
        cbar=True,
        linewidths=0.3,
        linecolor='#eeeeee'
    )

    plt.title("Trump vs Harris – Vorteil je Woche und Bundesstaat", fontsize=14)
    plt.ylabel("Bundesstaat")
    plt.xlabel("")
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    print(f"✔ Saved: {OUTPUT_PATH}")

async def main():
    raw_data = await fetch_data()
    table = preprocess(raw_data)
    plot_heatmap(table)

if __name__ == "__main__":
    asyncio.run(main())