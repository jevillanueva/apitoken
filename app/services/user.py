from datetime import datetime

from pymongo.collection import ReturnDocument

from app.core.database import db
from app.models.user import UserInDB
from app.utils import PyObjectId


class UserService:
    """Service for USERS in database operations"""
    TABLE = db.user
    @classmethod
    def insert_or_update_user(cls, user: UserInDB) -> PyObjectId | None:
        """Insert or update user in database

        Args:
            user (UserInDB): User to insert or update

        Returns:
            ObjectId | None: ObjectId of inserted or updated user or None if error
        """
        if hasattr(user, "id"):
            delattr(user, "id")
        find = UserService.get_user_by_email(user.email)
        if find is None:
            user.date_insert = datetime.utcnow()
            ret = cls.TABLE.insert_one(user.model_dump(by_alias=True))
            return ret.inserted_id
        else:
            if hasattr(user, "date_insert"):
                delattr(user, "date_insert")
            if hasattr(user, "admin"):
                delattr(user, "admin")
            if hasattr(user, "username"):
                delattr(user, "username")
            user.date_update = datetime.utcnow()
            user.disabled = find.disabled
            ret = cls.TABLE.find_one_and_update(
                {"email": user.email},
                {"$set": user.model_dump(by_alias=True)},
                return_document=ReturnDocument.AFTER,
            )
            return UserInDB(**ret).id

    @classmethod
    def get_user_by_email(cls, email: str) -> UserInDB | None:
        """Get user from database by email
        Args:
            email (str): email of user to find

        Returns:
            UserInDB | None: User information if found else None
        """
        ret = cls.TABLE.find_one({"email": email})
        if ret is not None:
            return UserInDB(**ret)
        else:
            return None
