from pydantic import BaseModel, ConfigDict


class TableBase(BaseModel):
    name: str
    capacity: int


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
