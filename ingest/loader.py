# ingest/loader.py
import csv
from datetime import datetime
from pathlib import Path 
from typing import List
from app.models import PresidentPredictionCreate, SenatePredictionCreate

def load_data_prediction() -> List[PresidentPredictionCreate]:
    predictions = []
    csv_path = Path().parent.parent / 'sample_data' / 'president_sample.csv'

    with csv_path.open('r', encoding='utf-8') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            
            prediction = PresidentPredictionCreate(
                date = datetime.strptime(row['Date (UTC)'], "%m-%d-%Y %H:%M" ),
                timestamp=int(row['Timestamp (UTC)']),
                democratic=float(row['Democratic']),
                trump=float(row['Donald Trump']),
                other=float(row['Other']),
                state=row['state']
            )
            predictions.append(prediction)

    return predictions
    #test für load_data_prediction 
    	#from ingest.loader import load_data_prediction
    	#predictions = load_data_prediction()


def load_data_senate(state_code: str) -> List[SenatePredictionCreate]:
	predictions = []

	csv_path = Path().parent.parent / 'sample_data' / 'senate' / f"{state_code}.csv"

	if not csv_path.exists():
		raise FileNotFoundError(f"Die Datei für den Staat {state_code} wurde nicht gefunden")

	with csv_path.open('r', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')

		headers = reader.fieldnames
		if headers is None:
			raise ValueError("Datei ist leer oder enthält keine Header")

		non_candidate_columns = {'Date (UTC)', 'Timestamp (UTC)', 'Other'}
		candidate_columns = [col for col in headers if col not in non_candidate_columns]

		if len(candidate_columns) != 2:
			raise ValueError(f"2 Kandidatenspalten wurden in der Datei {csv_path.name} erwartet, gefunden: {candidate_columns}")

		candidate_1_name, candidate_2_name = candidate_columns

		for row in reader:
			prediction = SenatePredictionCreate(
				date=datetime.strptime(row['Date (UTC)'], "%m-%d-%Y %H:%M"),
                timestamp=int(row['Timestamp (UTC)']),
                candidate_1=float(row[candidate_1_name]),
                candidate_1_name=candidate_1_name,
                candidate_2=float(row[candidate_2_name]),
                candidate_2_name=candidate_2_name,
                other=float(row['Other']),
                state=state_code.upper()
                )


			predictions.append(prediction)

	return predictions 