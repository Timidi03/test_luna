from abc import ABC, abstractmethod
from typing import List, Tuple

from src.models.organization import Organization


class AbstractOrganizationRepository(ABC):
    @abstractmethod
    async def get_by_id(self, organization_id: int) -> Organization: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> List[Organization]: ...

    @abstractmethod
    async def get_by_building_id(self, building_id: int) -> List[Organization]: ...

    @abstractmethod
    async def get_by_building_address(
        self, building_address: str
    ) -> List[Organization]: ...

    @abstractmethod
    async def get_by_activity_id(self, activity_id: int) -> List[Organization]: ...

    @abstractmethod
    async def get_by_activity_name(self, activity_name: str) -> List[Organization]: ...

    @abstractmethod
    async def get_by_activity_id_tree(self, activity_id: int) -> List[Organization]: ...

    @abstractmethod
    async def get_by_activity_name_tree(
        self, activity_name: str
    ) -> List[Organization]: ...

    @abstractmethod
    async def get_by_radius(
        self, radius: float, center: Tuple[float, float]
    ) -> List[Organization]: ...

    @abstractmethod
    async def get_by_box(
        self, box: Tuple[float, float, float, float]
    ) -> List[Organization]: ...
