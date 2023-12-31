import pytest
from unittest.mock import Mock, AsyncMock
from app.user.controllers import user_controller
from app.database.schemas import CandidateCreate, CustomerCreate, UserCredentials


class TestUserController:
    @pytest.mark.asyncio
    async def test_create_candidate(self):
        mocked_service = Mock()
        mocked_service.create_candidate = AsyncMock()

        create_candidate_func = user_controller.initialize(mocked_service)[
            "create_candidate"
        ]

        candidate_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "password": "password123",
            "fullname": "John Doe",
            "soft_skills": ["Communication"],
            "tech_skills": ["Python"],
        }
        candidate = CandidateCreate(**candidate_data)

        await create_candidate_func(candidate)
        assert mocked_service.create_candidate.call_count == 1
        mocked_service.create_candidate.assert_called_once_with(candidate)

    @pytest.mark.asyncio
    async def test_create_customer(self):
        mocked_service = Mock()
        mocked_service.create_customer = AsyncMock()

        create_customer_func = user_controller.initialize(mocked_service)[
            "create_customer"
        ]

        customer_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "password": "password123",
            "name": "Compañia XYZ",
        }
        customer = CustomerCreate(**customer_data)

        await create_customer_func(customer)
        assert mocked_service.create_customer.call_count == 1
        mocked_service.create_customer.assert_called_once_with(customer)

    @pytest.mark.asyncio
    async def test_get_by_credentials(self):
        mocked_service = Mock()
        mocked_service.get_by_credentials = AsyncMock()

        get_by_credentials_func = user_controller.initialize(mocked_service)[
            "get_by_credentials"
        ]

        credentials_data = {"email": "test@example.com", "password": "password123"}
        credentials = UserCredentials(**credentials_data)

        await get_by_credentials_func(credentials)
        assert mocked_service.get_by_credentials.call_count == 1
        mocked_service.get_by_credentials.assert_called_once_with(credentials)
