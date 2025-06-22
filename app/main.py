# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from app.models import PresidentPredictionCreate, SenatePredictionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import PresidentPredictionDB, SenatePredictionDB
from app.db.engine import get_session


app = FastAPI()


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
