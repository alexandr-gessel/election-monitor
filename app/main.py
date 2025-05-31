# app/main.py
from fastapi import FastAPI
from typing import List
from app.models import PresidentPrediction, SenatePrediction
from ingest.loader  import load_data_prediction, load_data_senate

app = FastAPI()

@app.get("/president/{state}")
def get_president_predictions(state_code: str) -> List[PresidentPrediction]:
	try:
		state_predictions = []
		predictions = load_data_prediction()
	
		for week_prediction in predictions:
			if week_prediction.state == state_code:
				state_predictions.append(week_prediction)

		if not state_predictions:
			raise HTTPException(status_code=404, detail=f"No data for state {state}")

		return state_predictions
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.get("/senate/{state_code}")
def get_senate_predictions(state_code: str):
	try:
		return load_data_senate(state_code)
	except FileNotFoundError:
		raise HTTPException(status_code=404, detail=f"Keine Senatsdaten für den Staat {state_code}")
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))