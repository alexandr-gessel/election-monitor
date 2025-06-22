# models for data-election
from pydantic import BaseModel
from datetime import datetime

class PresidentPredictionCreate(BaseModel):
	
	date : datetime
	timestamp : int
	democratic : float
	trump : float
	other : float
	state : str
	


class SenatePredictionCreate(BaseModel):
	date : datetime
	timestamp : int
	candidate_1 : float
	candidate_1_name : str
	candidate_2 : float
	candidate_2_name : str 
	other : float
	state : str