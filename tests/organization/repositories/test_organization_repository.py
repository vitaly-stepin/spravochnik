from unittest.mock import AsyncMock, MagicMock
import pytest
from app.organization.repositories.organization_repository import OrganizationRepository
from app.organization.models.organization import Organization

"""
Базовые юнит тесты для OrganizationRepository.
Покрыл базовый позитивный и негативный сценарии, просто чтобы показать понимание необходимосты покрытия кода тестами.
Хорошее покрытие в реальном включало бы в себя множество различных сценариев, входных данных итд.
"""


@pytest.fixture
def mock_db() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def repository(mock_db: AsyncMock) -> OrganizationRepository:
    return OrganizationRepository(mock_db)


@pytest.fixture
def mock_organization() -> MagicMock:
    org = MagicMock(spec=Organization)
    org.id = 1
    org.name = "Test Org"
    org.building_id = 1
    return org


class TestGetWithRelations:
    async def test_returns_organization(self, repository: OrganizationRepository, mock_db: AsyncMock, mock_organization: MagicMock) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_organization
        mock_db.execute.return_value = mock_result

        result = await repository.get_with_relations(1)

        assert result == mock_organization
        mock_db.execute.assert_awaited_once()

    async def test_returns_none_not_found(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        result = await repository.get_with_relations(999)

        assert result is None


class TestGetByName:
    async def test_returns_organization(self, repository: OrganizationRepository, mock_db: AsyncMock, mock_organization: MagicMock) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_organization
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_name("Test Org")

        assert result == mock_organization
        mock_db.execute.assert_awaited_once()

    async def test_returns_none_not_found(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_name("Nonexistent")

        assert result is None


class TestGetAllWithRelations:
    async def test_returns_organizations(self, repository: OrganizationRepository, mock_db, mock_organization):
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_organization]
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_all_with_relations()

        assert len(result) == 1
        assert result[0] == mock_organization
        mock_db.execute.assert_awaited_once()

    async def test_returns_empty_list(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_all_with_relations()

        assert result == []


class TestGetByBuildingId:
    async def test_returns_organizations(self, repository: OrganizationRepository, mock_db: AsyncMock, mock_organization):
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_organization]
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_building_id(1)

        assert len(result) == 1
        mock_db.execute.assert_awaited_once()

    async def test_returns_empty_not_found(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_building_id(999)

        assert result == []


class TestGetByActivityIds:
    async def test_returns_organizations(self, repository: OrganizationRepository, mock_db: AsyncMock, mock_organization: MagicMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_organization]
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_activity_ids([1, 2])

        assert len(result) == 1
        mock_db.execute.assert_awaited_once()

    async def test_returns_empty_not_found(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_by_activity_ids([999])

        assert result == []


class TestGetInCoordinateBounds:
    async def test_returns_organizations(self, repository: OrganizationRepository, mock_db: AsyncMock, mock_organization: MagicMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_organization]
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_in_coordinate_bounds(55.0, 56.0, 37.0, 38.0)

        assert len(result) == 1
        mock_db.execute.assert_awaited_once()

    async def test_returns_empty_no_matches(self, repository: OrganizationRepository, mock_db: AsyncMock) -> None:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await repository.get_in_coordinate_bounds(0.0, 0.1, 0.0, 0.1)

        assert result == []
