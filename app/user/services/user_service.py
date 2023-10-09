from app.user.helpers.user_helper import UserHelper
from app.database.schemas import User, CandidateCreate
from app.user.repositories.user_repository import UserRepository


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
        # TODO: Add new candidate event
        return User.model_validate(saved_user)
