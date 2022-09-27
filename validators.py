from datetime import date

from pydantic import BaseModel, validator

from airports import load_airports


class FlightValidator(BaseModel):
    departure_date: date
    origin: str
    destination: str

    @validator('departure_date')
    def more_than_today(cls, v):
        if v < date.today():
            raise ValueError('Departure must be today or more.')
        return v

    @validator('origin', 'destination')
    def check_airports(cls, v, values, field):
        if load_airports().get(v) is None:
            raise ValueError(f'{field.name.upper()} not found.')
        return v