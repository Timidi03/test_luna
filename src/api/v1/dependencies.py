from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.repositories.abstract_organization import AbstractOrganizationRepository
from src.repositories.organization_repository import OrganizationRepository
from src.services.abstract_organization_service import AbstractOrganizationService
from src.services.organization_service import OrganizationService


async def get_organization_repo(
    session: AsyncSession = Depends(get_db),
) -> AbstractOrganizationRepository:
    return OrganizationRepository(session)


async def get_organization_service(
    repo: OrganizationRepository = Depends(get_organization_repo),
) -> AbstractOrganizationService:
    return OrganizationService(repo)
