from fastapi import APIRouter, Depends
from typing import TYPE_CHECKING
from app.database.schemas import User, CandidateCreate, CustomerCreate, UserCredentials

if TYPE_CHECKING:
    from app.user.services.user_service import UserService


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


def initialize(user_service: "UserService"):
    @router.post("/candidate")
    async def create_candidate(candidate: CandidateCreate) -> User:
        return await user_service.create_candidate(candidate)

    @router.post("/customer")
    async def create_customer(customer: CustomerCreate) -> User:
        return await user_service.create_customer(customer)

    @router.get("/by-credentials")
    async def get_by_credentials(query: UserCredentials = Depends()) -> User:
        return await user_service.get_by_credentials(query)

    return {
        "create_candidate": create_candidate,
        "create_customer": create_customer,
        "get_by_credentials": get_by_credentials,
    }
