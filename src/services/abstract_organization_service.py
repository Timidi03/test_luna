from abc import ABC, abstractmethod
from typing import List, Tuple

from src.schemas.organization import OrganizationResponse


class AbstractOrganizationService(ABC):
    @abstractmethod
    async def get_by_id(self, organization_id: int) -> OrganizationResponse: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> List[OrganizationResponse]: ...

    @abstractmethod
    async def get_by_building_id_or_address(
        self, building_id: int | None = None, building_address: str | None = None
    ) -> List[OrganizationResponse]: ...

    @abstractmethod
    async def get_by_activity_id_or_name(
        self, activity_id: int | None = None, activity_name: str | None = None
    ) -> List[OrganizationResponse]: ...

    @abstractmethod
    async def get_by_activity_id_or_name_tree(
        self, activity_id: int | None = None, activity_name: str | None = None
    ) -> List[OrganizationResponse]: ...

    @abstractmethod
    async def get_by_radius(
        self, radius: float, center: Tuple[float, float]
    ) -> List[OrganizationResponse]: ...

    @abstractmethod
    async def get_by_box(
        self, box: Tuple[float, float, float, float]
    ) -> List[OrganizationResponse]: ...
