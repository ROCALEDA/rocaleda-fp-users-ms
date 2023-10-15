from app.database import models, database


class UserRepository:
    async def create_user(self, new_user: dict) -> models.User:
        db_user = models.User(**new_user)

        with database.create_session() as db:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        return db_user
