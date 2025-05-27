from typing import Annotated
from datetime import date as dt_date

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from app.services import fetch_flight_events
from app.utils import generate_valid_journeys

app = FastAPI()


class Journey(BaseModel):
    date: dt_date = Field("2021-12-31", format="%Y-%m-%d")
    from_: str = Field("MAD", max_length=3)
    to: str = Field("BUE", max_length=3)

@app.get("/journeys/search")
async def search_journeys(search_query: Annotated[Journey, Query()]):
    events = await fetch_flight_events()
    journeys = generate_valid_journeys(events, search_query.date, search_query.from_.upper(), search_query.to.upper())
    return journeys
