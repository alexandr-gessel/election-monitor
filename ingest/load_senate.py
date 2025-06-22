# ingest/load_senate.py

import csv
from pathlib import Path
from datetime import datetime

from app.db.engine import async_session
from app.db.session import SenatePredictionDB


def parse_senate_csv(file_path: Path, state: str):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        print(f"{file_path.name}: заголовки = {reader.fieldnames}")
        header = reader.fieldnames[2:]

        if 'Democrat' in header and 'Republican' in header:
            candidate_1_name = 'Democrat'
            candidate_2_name = 'Republican'
        else:
            candidate_1_name = header[0]
            candidate_2_name = header[1]

        other_col = header[2] if len(header) > 2 else 'Other'

        records = []
        for row in reader:
            dt = datetime.strptime(row['Date (UTC)'], "%m-%d-%Y %H:%M")
            timestamp = int(row['Timestamp (UTC)'])
            record = {
                'date': dt,
                'timestamp': timestamp,
                'candidate_1': float(row[header[0]] or 0.0),
                'candidate_1_name': candidate_1_name,
                'candidate_2': float(row[header[1]] or 0.0),
                'candidate_2_name': candidate_2_name,
                'other': float(row.get(other_col, 0.0) or 0.0),
                'state': state.upper()
            }
            records.append(record)
        return records


async def insert_bulk(records):
    async with async_session() as session:
        for data in records:
            prediction = SenatePredictionDB(**data)
            session.add(prediction)
        await session.commit()


async def main():
    data_dir = Path("sample_data/senate")
    all_records = []

    for file in data_dir.glob("*.csv"):
        state = file.stem
        records = parse_senate_csv(file, state)
        all_records.extend(records)

    await insert_bulk(all_records)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())