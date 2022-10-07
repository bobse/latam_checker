from datetime import date

from pydantic import BaseModel, validator, constr, condate

from airports import load_airports


class FlightData(BaseModel):
    departure_date: condate(ge=date.today())
    origin: constr(to_upper=True)
    destination: constr(to_upper=True)

    @validator('origin', 'destination')
    def check_airports_on_db(cls, v, values, field):
        if load_airports().get(v) is None:
            raise ValueError(f'{field.name.upper()} not found.')
        return v

    @validator('destination')
    def check_airports_not_equal(cls, v, values, field):
        if v == values.get('origin'):
            raise ValueError(f'Origin and destination airports must be diferent')
        return v
