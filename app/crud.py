from typing import List

from fastapi import HTTPException
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Building


async def create_building_orm(address: str) -> Building:
    async with AsyncSessionLocal() as session:
        building = Building(address=address)
        session.add(building)
        await session.commit()
        return building


async def get_all_building_orm() -> List[Building]:
    async with AsyncSessionLocal() as session:
        query = select(Building)
        result = await session.execute(query)
        return result.scalars().all()


async def get_building_orm(pk) -> Building:
    async with AsyncSessionLocal() as session:
        obj = select(Building).filter(Building.id == pk)
        result = await session.execute(obj)
        return result.scalar_one()


async def delete_building_orm(pk) -> None:
    async with AsyncSessionLocal() as session:
        obj = await get_building_orm(pk)
        if obj:
            await session.delete(obj)
            await session.commit()
