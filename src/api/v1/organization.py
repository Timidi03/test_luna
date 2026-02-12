from typing import List

from fastapi import Depends, Path, Query
from fastapi.routing import APIRouter

from src.api.v1.dependencies import get_organization_service
from src.api.v1.organization_docs import *
from src.core.constants import (
    EARTH_RADIUS,
    MAX_LAT,
    MAX_LENGTH_STRING,
    MAX_LON,
    MIN_ID,
    MIN_LAT,
    MIN_LENGTH_STRING,
    MIN_LON,
)
from src.schemas.organization import OrganizationBox, OrganizationResponse
from src.services.abstract_organization_service import AbstractOrganizationService

router = APIRouter(prefix="/search")


@router.get("/name", response_model=List[OrganizationResponse], **SEARCH_BY_NAME_DOC)
async def get_organizations_by_name(
    name: str = Query(
        ...,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Часть или полное название организации (поиск без учета регистра)",
        examples=["техСофт"],
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_name(name)


@router.get(
    "/building", response_model=List[OrganizationResponse], **SEARCH_BY_BUILDING_DOC
)
async def get_organizations_by_building(
    building_id: int | None = Query(
        None, ge=MIN_ID, description="Идентификатор здания", examples=[1]
    ),
    building_address: str | None = Query(
        None,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Полный адрес здания",
        examples=["г. Москва, ул. Ленина 1"],
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_building_id_or_address(building_id, building_address)


@router.get(
    "/activity", response_model=List[OrganizationResponse], **SEARCH_BY_ACTIVITY_DOC
)
async def get_organizations_by_activity(
    activity_id: int | None = Query(
        None, ge=MIN_ID, description="Идентификатор вида деятельности", examples=[1]
    ),
    activity_name: str | None = Query(
        None,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Название вида деятельности",
        examples=["Еда"],
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_activity_id_or_name(activity_id, activity_name)


@router.get(
    "/activity-tree",
    response_model=List[OrganizationResponse],
    **SEARCH_BY_ACTIVITY_TREE_DOC,
)
async def get_organizations_by_activity_tree(
    activity_id: int | None = Query(
        None, ge=MIN_ID, description="Идентификатор вида деятельности", examples=[1]
    ),
    activity_name: str | None = Query(
        None,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Название вида деятельности",
        examples=["Еда"],
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_activity_id_or_name_tree(activity_id, activity_name)


@router.get(
    "/radius", response_model=List[OrganizationResponse], **SEARCH_BY_RADIUS_DOC
)
async def get_organizations_by_radius(
    latitude: float = Query(
        ...,
        ge=MIN_LAT,
        le=MAX_LAT,
        description="Широта центра поиска",
        examples=[55.7558],
    ),
    longitude: float = Query(
        ...,
        ge=MIN_LON,
        le=MAX_LON,
        description="Долгота центра поиска",
        examples=[37.6176],
    ),
    radius: float = Query(
        ...,
        gt=0,
        le=EARTH_RADIUS,
        description="Радиус поиска в метрах",
        examples=[5000],
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_radius(radius, (latitude, longitude))


@router.get("/box", response_model=List[OrganizationResponse], **SEARCH_BY_BOX_DOC)
async def get_organizations_by_box(
    box: OrganizationBox = Query(...),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_box(
        (box.lat_min, box.lon_min, box.lat_max, box.lon_max)
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse | None,
    **GET_ORGANIZATION_BY_ID_DOC,
)
async def get_organization_info(
    organization_id: int = Path(
        ..., ge=MIN_ID, description="Идентификатор организации", examples=[1]
    ),
    service: AbstractOrganizationService = Depends(get_organization_service),
):
    return await service.get_by_id(organization_id)
