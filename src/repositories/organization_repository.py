from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.constants import EARTH_RADIUS
from src.models.activity import Activity
from src.models.building import Building
from src.models.organization import Organization
from src.repositories.abstract_organization import AbstractOrganizationRepository


class OrganizationRepository(AbstractOrganizationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, organization_id: int) -> Organization:
        query = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(*self._base_options())
        )

        return await self._execute_one(query)

    async def get_by_name(self, name: str) -> List[Organization]:
        query = (
            select(Organization)
            .where(func.lower(Organization.name).contains(name.lower()))
            .options(*self._base_options())
        )

        return await self._execute_many(query)

    async def get_by_building_id(self, building_id: int) -> List[Organization]:
        query = (
            select(Organization)
            .join(Organization.building)
            .where(Building.id == building_id)
            .options(*self._base_options())
        )

        return await self._execute_many(query)

    async def get_by_building_address(
        self, building_address: str
    ) -> List[Organization]:
        building_id = await self._get_building_id_by_address(building_address)
        if building_id:
            return await self.get_by_building_id(building_id)
        return []

    async def get_by_activity_id(self, activity_id) -> List[Organization]:
        query = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
            .options(*self._base_options())
        )

        return await self._execute_many(query)

    async def get_by_activity_name(self, activity_name: str) -> List[Organization]:
        activity_id = await self._get_activity_id_by_name(activity_name)
        if activity_id:
            return await self.get_by_activity_id(activity_id)
        return []

    async def get_by_activity_id_tree(self, activity_id: int) -> List[Organization]:
        path = await self._get_activity_path_by_id(activity_id)
        query = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.path.startswith(path))
            .options(*self._base_options())
            .distinct()
        )

        return await self._execute_many(query)

    async def get_by_activity_name_tree(self, activity_name: str) -> List[Organization]:
        activity_id = await self._get_activity_id_by_name(activity_name)
        if not activity_id:
            return []
        return await self.get_by_activity_id_tree(activity_id)

    async def get_by_radius(
        self,
        radius: float,
        center: Tuple[float, float],
    ) -> List[Organization]:
        distance = self._get_distance_expression(center)
        query = (
            select(Organization)
            .join(Organization.building)
            .where(distance <= radius)
            .options(*self._base_options())
        )

        return await self._execute_many(query)

    async def get_by_box(
        self, box: Tuple[float, float, float, float]
    ) -> List[Organization]:
        min_lat, min_lon, max_lat, max_lon = box
        query = (
            select(Organization)
            .join(Organization.building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
            .options(*self._base_options())
        )

        return await self._execute_many(query)

    @staticmethod
    def _get_distance_expression(center: Tuple[float, float]):
        lat, lon = center
        distance_expr = EARTH_RADIUS * func.acos(
            func.cos(func.radians(lat))
            * func.cos(func.radians(Building.latitude))
            * func.cos(func.radians(Building.longitude) - func.radians(lon))
            + func.sin(func.radians(lat)) * func.sin(func.radians(Building.latitude))
        )
        return distance_expr

    async def _get_building_id_by_address(self, address: str) -> int | None:
        query = select(Building.id).where(
            func.lower(Building.address) == f"{address.lower()}"
        )

        return await self._execute_one(query)

    async def _get_activity_id_by_name(self, name: str) -> int | None:
        query = select(Activity.id).where(
            func.lower(Activity.name) == f"{name.lower()}"
        )

        return await self._execute_one(query)

    async def _get_activity_path_by_id(self, activity_id) -> str:
        query = select(Activity.path).where(Activity.id == activity_id)

        return await self._execute_one(query)

    @staticmethod
    def _base_options():
        return (
            selectinload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones),
        )

    async def _execute_one(self, query):
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _execute_many(self, query):
        result = await self.session.execute(query)
        return result.scalars().unique().all()
