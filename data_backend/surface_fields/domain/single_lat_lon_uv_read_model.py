from pydantic import BaseModel


class SingleLatLonUVReadModel(BaseModel):
    latitude: str
    longitude: str
    u_velocity: str
    v_velocity: str
