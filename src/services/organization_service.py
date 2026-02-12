from typing import List, Tuple

from src.core.exceptions import NotFoundError, ServiceError, ValidationError
from src.core.logger import get_logger
from src.repositories.abstract_organization import AbstractOrganizationRepository
from src.schemas.organization import OrganizationResponse
from src.services.abstract_organization_service import AbstractOrganizationService

logger = get_logger(__name__)


class OrganizationService(AbstractOrganizationService):
    def __init__(self, repo: AbstractOrganizationRepository):
        self.repo = repo

    async def get_by_id(self, organization_id: int) -> OrganizationResponse:
        try:
            org = await self.repo.get_by_id(organization_id)
            if not org:
                raise NotFoundError(f"Organization with id={organization_id} not found")
            logger.debug(
                f"Organization with id={organization_id} retrieved successfully"
            )
            return org

        except NotFoundError as nf:
            logger.warning(nf.message)
            raise

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organization with id={organization_id}"
            ) from e

    async def get_by_name(self, name: str) -> List[OrganizationResponse]:
        try:
            orgs = await self.repo.get_by_name(name)
            if not orgs:
                logger.info(f"No organizations found for name={name}")
                return orgs
            logger.debug(f"Organizations with name={name} retrieved successfully")
            return orgs

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organizations with name={name}"
            ) from e

    async def get_by_building_id_or_address(
        self, building_id: int | None = None, building_address: str | None = None
    ) -> List[OrganizationResponse]:

        try:
            if (
                building_id is None
                and building_address is None
                or building_id is not None
                and building_address is not None
            ):
                raise ValidationError("Exactly one parameter must be provided")
            elif building_id:
                orgs = await self.repo.get_by_building_id(building_id)
                if not orgs:
                    logger.info(
                        f"Organizations with building_id={building_id} not found"
                    )
                    return orgs
                logger.debug(f"Building with id={building_id} retrieved successfully")
                return orgs
            else:
                orgs = await self.repo.get_by_building_address(building_address)
                if not orgs:
                    logger.info(
                        f"Organizations with address={building_address} not found"
                    )
                    return orgs
                logger.debug(
                    f"Building with address={building_address} retrieved successfully"
                )
                return orgs

        except ValidationError as ve:
            logger.exception(ve.message)
            raise

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organizations with building_id={building_id} or building_address={building_address}"
            ) from e

    async def get_by_activity_id_or_name(
        self, activity_id: int | None = None, activity_name: str | None = None
    ) -> List[OrganizationResponse]:
        try:
            if (
                activity_id is None
                and activity_name is None
                or activity_id is not None
                and activity_name is not None
            ):
                raise ValidationError("Exactly one parameter must be provided")
            elif activity_id:
                orgs = await self.repo.get_by_activity_id(activity_id)
                if not orgs:
                    logger.info(
                        f"Organizations with activity_id={activity_id} not found"
                    )
                    return orgs
                logger.debug(f"Activity with id={activity_id} retrieved successfully")
                return orgs
            else:
                orgs = await self.repo.get_by_activity_name(activity_name)
                if not orgs:
                    logger.info(
                        f"Organizations with activity_name={activity_name} not found"
                    )
                    return orgs
                logger.debug(
                    f"Activity with name={activity_name} retrieved successfully"
                )
                return orgs

        except ValidationError as ve:
            logger.exception(ve.message)
            raise

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organizations with activity_id={activity_id} or activity_name={activity_name}"
            ) from e

    async def get_by_activity_id_or_name_tree(
        self, activity_id: int | None = None, activity_name: str | None = None
    ) -> List[OrganizationResponse]:
        try:
            if (
                activity_id is None
                and activity_name is None
                or activity_id is not None
                and activity_name is not None
            ):
                raise ValidationError("Exactly one parameter must be provided")
            elif activity_id:
                orgs = await self.repo.get_by_activity_id_tree(activity_id)
                if not orgs:
                    logger.info(
                        f"Organizations with activity_id={activity_id} not found"
                    )
                    return orgs
                logger.debug(f"Activity with id={activity_id} retrieved successfully")
                return orgs
            else:
                orgs = await self.repo.get_by_activity_name_tree(activity_name)
                if not orgs:
                    logger.info(
                        f"Organizations with activity_name={activity_name} and subactivities not found"
                    )
                logger.debug(
                    f"Activity with name={activity_name} and subactivities retrieved successfully"
                )
                return orgs

        except ValidationError as ve:
            logger.exception(ve.message)
            raise

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organizations with activity_id={activity_id} or activity_name={activity_name}"
            ) from e

    async def get_by_radius(
        self, radius: float, center: Tuple[float, float]
    ) -> List[OrganizationResponse]:
        try:
            orgs = await self.repo.get_by_radius(radius, center)
            if not orgs:
                logger.info(
                    f"No Organizations in this radius={radius} with center={center}"
                )
                return orgs
            logger.debug(
                f"Organizations in this radius={radius} with center={center} retrieved successfully"
            )
            return orgs

        except Exception as e:
            logger.exception(e)
            raise ServiceError(
                f"Error retrieving organizations in this radius={radius} with center={center} "
            ) from e

    async def get_by_box(
        self, box: Tuple[float, float, float, float]
    ) -> List[OrganizationResponse]:
        if box[0] >= box[2]:
            raise ValidationError("lat_min должно быть меньше lat_max")
        if box[1] >= box[3]:
            raise ValidationError("lon_min должно быть меньше lon_max")
        try:
            orgs = await self.repo.get_by_box(box)
            if not orgs:
                logger.info(f"No Organizations in this box={box}")
                return orgs
            logger.debug(f"Organizations in this box={box} retrieved successfully")
            return orgs

        except ValidationError as ve:
            logger.exception(ve.message)
            raise

        except Exception as e:
            logger.exception(e)
            raise ServiceError(f"Error retrieving organizations in this box={box} ")
