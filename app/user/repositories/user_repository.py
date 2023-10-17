from app.database import models, database


class UserRepository:
    async def create_user(self, new_user: dict) -> models.User:
        db_user = models.User(**new_user)

        with database.create_session() as db:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        return db_user

    async def get_by_email(self, email: str) -> models.User:
        with database.create_session() as db:
            found_user = db.query(models.User).filter_by(email=email).first()

        return found_user
