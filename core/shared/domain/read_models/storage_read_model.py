from pydantic import BaseModel


class StorageReadModel(BaseModel):
    total: int
    used: int
