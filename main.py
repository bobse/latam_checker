from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.responses import FileResponse

from airports import load_airports
from latam import convert_to_matrix, get_all_dates
from settings import ORIGINS
from validators import FlightValidator

AIRPORTS = load_airports()

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
        FlightValidator(
                **locals()
        )
    except ValidationError as e:
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = e.errors().__str__(),
        )
    try:
        flights, best_price = get_all_dates(departure_date, origin, destination)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not get the results. Please try again",
        )
    # for testing
    # best_price = 1770.8
    # with open("./response.json", "r") as file:
    #     flights = json.load(file)
    key_map, matrix = convert_to_matrix(flights)
    return {"flights_matrix": matrix, "key_map": key_map, "best_price": best_price}


@app.get("/airports")
def get_airports():
    return AIRPORTS
