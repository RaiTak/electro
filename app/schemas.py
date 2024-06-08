from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True
