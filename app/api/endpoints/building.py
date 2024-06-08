from typing import List

from fastapi import APIRouter, HTTPException
from app.crud import create_building_orm, get_all_building_orm, get_building_orm, delete_building_orm
from app.schemas import BuildingCreate, Building

router = APIRouter()


@router.post("/buildings/create/", response_model=Building)
async def create_building_endpoint(building: BuildingCreate):
    return await create_building_orm(building.address)


@router.get("/buildings/", response_model=List[Building])
async def get_all_building_endpoint() -> List[Building]:
    buildings = await get_all_building_orm()
    return buildings


@router.get("/buildings/{pk}", response_model=Building)
async def get_building_endpoint(pk: int) -> Building:
    obj = await get_building_orm(pk)
    return obj


@router.delete("/buildings/delete/{pk}")
async def delete_building_endpoint(pk: int):
    await delete_building_orm(pk)
