from fastapi import APIRouter

from app.database.schemas import User, CandidateCreate
from app.user.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


def initialize(user_service: UserService):
    @router.post("/candidate")
    async def create_candidate(candidate: CandidateCreate) -> User:
        user = await user_service.create_candidate(candidate)
        return user

    return {"create_candidate": create_candidate}
