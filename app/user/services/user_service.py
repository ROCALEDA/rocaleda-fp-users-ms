import json
from app.user.helpers.user_helper import UserHelper
from app.database.schemas import User, CandidateCreate
from app.user.repositories.user_repository import UserRepository
from app.commons.gcp import publisher, CANDIDATE_CREATION_TOPIC_PATH


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_candidate(self, new_user: CandidateCreate) -> User:
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

        message_future = publisher.publish(
            CANDIDATE_CREATION_TOPIC_PATH, new_candidate_message
        )
        message_future.result()

        return User.model_validate(saved_user)
