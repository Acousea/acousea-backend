from pydantic import BaseModel


class StorageReadModel(BaseModel):
    total: int
    free: int
