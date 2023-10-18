import json
from typing import TYPE_CHECKING

from fastapi import HTTPException
from app.user.helpers.user_helper import UserHelper
from app.database.schemas import User, CandidateCreate, CustomerCreate, UserCredentials
from app.commons.gcp import (
    get_publisher,
    get_candidate_creation_topic_path,
    get_customer_creation_topic_path,
)

if TYPE_CHECKING:
    from app.user.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: "UserRepository"):
        self.user_repository = user_repository
        self.publisher = get_publisher()

    async def create_candidate(self, new_user: CandidateCreate) -> User:
        existing_user = await self.user_repository.get_by_email(new_user.email)

        if existing_user is not None:
            raise HTTPException(400, "Email already in use")

        new_user.password = UserHelper.hash_password(new_user.password)
        saved_user = await self.user_repository.create_user(
            {
                "email": new_user.email,
                "phone": new_user.phone,
                "role_id": new_user.role_id,
                "password": new_user.password,
            }
        )

        new_candidate_data = {
            "user_id": saved_user.id,
            "fullname": new_user.fullname,
            "soft_skills": new_user.soft_skills,
            "tech_skills": new_user.tech_skills,
        }

        new_candidate_message = json.dumps(new_candidate_data).encode("utf-8")

        message_future = self.publisher.publish(
            get_candidate_creation_topic_path(self.publisher), new_candidate_message
        )
        message_future.result()

        return User.model_validate(saved_user)

    async def create_customer(self, new_user: CustomerCreate) -> User:
        new_user.password = UserHelper.hash_password(new_user.password)
        saved_user = await self.user_repository.create_user(
            {
                "email": new_user.email,
                "phone": new_user.phone,
                "role_id": new_user.role_id,
                "password": new_user.password,
            }
        )

        new_customer_data = {
            "user_id": saved_user.id,
            "name": new_user.name,
        }

        new_customer_message = json.dumps(new_customer_data).encode("utf-8")

        message_future = self.publisher.publish(
            get_customer_creation_topic_path(self.publisher), new_customer_message
        )
        message_future.result()

        return User.model_validate(saved_user)

    async def get_by_credentials(self, credentials: UserCredentials) -> User:
        user = await self.user_repository.get_by_email(credentials.email)

        if user is None:
            raise HTTPException(400, "Invalid credentials")

        is_password_correct = UserHelper.verify_password(
            credentials.password, user.password
        )

        if not is_password_correct:
            raise HTTPException(400, "Invalid credentials")

        return User.model_validate(user)
