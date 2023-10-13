import pytest
from unittest.mock import Mock, AsyncMock
from app.user.controllers import user_controller
from app.database.schemas import CandidateCreate


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
