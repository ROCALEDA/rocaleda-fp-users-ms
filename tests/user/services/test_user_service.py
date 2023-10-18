import json
import pytest
import bcrypt
from unittest.mock import Mock, AsyncMock, patch, ANY
from app.database.schemas import CandidateCreate, CustomerCreate, UserCredentials
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

    @pytest.mark.asyncio
    @patch("app.user.services.user_service.get_publisher")
    @patch("app.user.services.user_service.get_customer_creation_topic_path")
    async def test_create_customer(
        self, mock_get_customer_creation_topic_path, mock_get_publisher
    ):
        mock_get_customer_creation_topic_path.return_value = Mock()

        mock_publisher = Mock()
        mock_publisher.publish = Mock()
        mock_get_publisher.return_value = mock_publisher

        mocked_repository = Mock()
        mocked_repository.create_user = AsyncMock()

        mocked_user = Mock(
            id=2, email="test2@example.com", phone="+12345678901", role_id=2
        )
        mocked_repository.create_user.return_value = mocked_user

        user_service = UserService(mocked_repository)

        customer_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "password": "password123",
            "name": "John Doe",
        }
        customer = CustomerCreate(**customer_data)

        await user_service.create_customer(customer)

        assert mocked_repository.create_user.call_count == 1
        mocked_repository.create_user.assert_called_once_with(
            {
                "email": customer.email,
                "phone": customer.phone,
                "role_id": customer.role_id,
                "password": customer.password,
            }
        )

        assert mock_publisher.publish.call_count == 1
        mock_publisher.publish.assert_called_once_with(
            ANY,
            json.dumps(
                {
                    "user_id": mocked_user.id,
                    "name": customer.name,
                }
            ).encode("utf-8"),
        )

    @pytest.mark.asyncio
    @patch("app.user.services.user_service.get_publisher")
    async def test_get_by_credentials(self, mock_get_publisher):
        mock_publisher = Mock()
        mock_publisher.publish = Mock()
        mock_get_publisher.return_value = mock_publisher

        password = bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        mocked_repository = Mock()
        mocked_repository.get_by_email = AsyncMock()
        mocked_repository.get_by_email.return_value = Mock(
            password=password,
            email="test@example.com",
            phone="+573223024121",
            role_id=1,
            id=1,
        )

        user_service = UserService(mocked_repository)

        credentials_data = {
            "email": "test@example.com",
            "password": "password",
        }
        credentials = UserCredentials(**credentials_data)

        response = await user_service.get_by_credentials(credentials)
