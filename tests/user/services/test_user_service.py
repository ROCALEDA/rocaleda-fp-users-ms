import json
import pytest
from unittest.mock import Mock, AsyncMock, patch, ANY
from app.database.schemas import CandidateCreate
from app.user.services.user_service import UserService


class TestUserService:
    @pytest.mark.asyncio
    @patch("app.user.services.user_service.get_publisher")
    @patch("app.user.services.user_service.get_candidate_creation_topic_path")
    async def test_create_candidate(
        self, mock_get_candidate_creation_topic_path, mock_get_publisher
    ):
        mock_get_candidate_creation_topic_path.return_value = Mock()

        mock_publisher = Mock()
        mock_publisher.publish = Mock()
        mock_get_publisher.return_value = mock_publisher

        mocked_repository = Mock()
        mocked_repository.create_user = AsyncMock()

        mocked_user = Mock(
            id=1, email="test@example.com", phone="+1234567890", role_id=3
        )
        mocked_repository.create_user.return_value = mocked_user

        user_service = UserService(mocked_repository)

        candidate_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "password": "password123",
            "fullname": "John Doe",
            "soft_skills": ["Communication"],
            "tech_skills": ["Python"],
        }
        candidate = CandidateCreate(**candidate_data)

        await user_service.create_candidate(candidate)

        assert mocked_repository.create_user.call_count == 1
        mocked_repository.create_user.assert_called_once_with(
            {
                "email": candidate.email,
                "phone": candidate.phone,
                "role_id": candidate.role_id,
                "password": candidate.password,
            }
        )

        assert mock_publisher.publish.call_count == 1
        mock_publisher.publish.assert_called_once_with(
            ANY,
            json.dumps(
                {
                    "user_id": mocked_user.id,
                    "fullname": candidate.fullname,
                    "soft_skills": candidate.soft_skills,
                    "tech_skills": candidate.tech_skills,
                }
            ).encode("utf-8"),
        )
