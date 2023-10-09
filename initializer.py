from fastapi import FastAPI

from app.database import models, database
from app.user.controllers import user_controller
from app.health.controllers import health_controller
from app.user.services.user_service import UserService
from app.health.services.health_service import HealthService
from app.user.repositories.user_repository import UserRepository


class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self.init_health_module()
        self.init_user_module()
        self.init_database()

    def init_health_module(self):
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)

    def init_user_module(self):
        user_repository = UserRepository()
        user_service = UserService(user_repository)
        user_controller.initialize(user_service)
        self.app.include_router(user_controller.router)

    def init_database(self):
        models.Base.metadata.create_all(bind=database.engine)
