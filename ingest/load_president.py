# ingest/load_president.py

import csv
from pathlib import Path
from datetime import datetime

from app.db.engine import async_session
from app.db.session import PresidentPredictionDB

DATA_PATH = Path("sample_data/president_sample.csv")


def parse_president_csv(file_path: Path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        records = []

        for row in reader:
            # date
            dt = datetime.strptime(row['Date (UTC)'], "%m-%d-%Y %H:%M")
            timestamp = int(row['Timestamp (UTC)'])

            record = {
                'date': dt,
                'timestamp': timestamp,
                'democratic': float(row['Democratic'] or 0.0),
                'trump': float(row['Donald Trump'] or 0.0 ),
                'other': float(row['Other'] or 0.0),
                'state': row['state'].strip().upper()
            }
            records.append(record)

        return records


async def insert_bulk(records):
    async with async_session() as session:
        for data in records:
            prediction = PresidentPredictionDB(**data)
            session.add(prediction)
        await session.commit()


async def main():
    records = parse_president_csv(DATA_PATH)
    print(f" {len(records)} aus {DATA_PATH.name}...")
    await insert_bulk(records)
    print(" alles klar! ")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())