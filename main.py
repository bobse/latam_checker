import json
import logging
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.responses import FileResponse

from airports import load_airports
from latam import LatamFinder
from settings import ORIGINS, LogConfig
from validators import FlightData

dictConfig(LogConfig().dict())
logger = logging.getLogger("app")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')


@app.get("/{departure_date}/{origin}/{destination}")
def get_flights(departure_date: str, origin: str, destination: str):
    try:
        FlightData(
                **locals()
        )
    except ValidationError as e:
        error_msg = json.loads(e.json())
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = error_msg
        )
    try:
        latam = LatamFinder(departure_date, origin, destination)
        latam.get_all_flights()
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not get the results. Please try again later",
        )

    if latam.best_price == float("inf"):
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Could not get flights for this destination or date",
        )

    return {"flights": latam.all_flights, "best_price": latam.best_price}


@app.get("/airports")
def get_airports():
    AIRPORTS = load_airports()
    if len(AIRPORTS) == 0:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Could not load the airport list",
        )
    return AIRPORTS


if __name__ == '__main__':
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
