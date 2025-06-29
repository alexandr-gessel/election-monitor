# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from app.models import PresidentPredictionCreate, SenatePredictionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import PresidentPredictionDB, SenatePredictionDB
from app.db.engine import get_session
from app.data.states import states
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def index(request: Request):
    
    available_files = set(os.listdir("app/static/charts"))

    both = []
    pres_only = []
    sen_only = []

    for code, name in states:
        pres = f"{code}_president.png" in available_files
        sen = f"{code}_senate.png" in available_files

        if pres and sen:
            both.append((code, name))
        elif pres:
            pres_only.append((code, name))
        elif sen:
            sen_only.append((code, name))

    sorted_states = both + pres_only + sen_only

    return templates.TemplateResponse("index.html", {"request": request, "states": sorted_states})

@app.get("/about.html")
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/state/{state}")
async def state_page(
    request: Request,
    state: str = Path(..., min_length=2, max_length=2),
    session: AsyncSession = Depends(get_session)
):
    # Presiden
    try:
        pres_query = select(PresidentPredictionDB).where(PresidentPredictionDB.state == state)
        pres_result = await session.execute(pres_query)
        pres_data = pres_result.scalars().all()
    except SQLAlchemyError:
        pres_data = []

    # Senate
    try:
        sen_query = select(SenatePredictionDB).where(SenatePredictionDB.state == state)
        sen_result = await session.execute(sen_query)
        sen_data = sen_result.scalars().all()
    except SQLAlchemyError:
        pres_data = []
    
    return templates.TemplateResponse("state.html", {
        "request": request,
        "state": state,
        "pres_data": pres_data,
        "sen_data": sen_data,
         "states": states
    })


@app.post("/president/")
async def create_president_prediction(
    prediction: PresidentPredictionCreate,
    session: AsyncSession = Depends(get_session)
):
    new_prediction = PresidentPredictionDB(**prediction.model_dump())

    session.add(new_prediction)
    await session.commit()
    await session.refresh(new_prediction)

    return new_prediction


@app.get("/president/{state}")
async def get_president_predictions(state: str, session: AsyncSession = Depends(get_session)):
    query = select(PresidentPredictionDB).where(PresidentPredictionDB.state == state)
    result = await session.execute(query)
    predictions = result.scalars().all()

    if not predictions:
        raise HTTPException(status_code=404, detail=f"No predictions found for state {state}")
    
    return predictions


@app.post("/senate/")
async def create_senate_prediction(
    prediction: SenatePredictionCreate,
    session: AsyncSession = Depends(get_session)
):
    new_prediction = SenatePredictionDB(**prediction.model_dump())

    session.add(new_prediction)
    await session.commit()
    await session.refresh(new_prediction)

    return new_prediction


@app.get("/senate/{state}")
async def get_senate_predictions(state: str, session: AsyncSession = Depends(get_session)):
    query = select(SenatePredictionDB).where(SenatePredictionDB.state == state)
    result = await session.execute(query)
    predictions = result.scalars().all()

    if not predictions:
        raise HTTPException(status_code=404, detail=f"No predictions found for state {state}")
    
    return predictions
