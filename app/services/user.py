from datetime import datetime

from pymongo.collection import ReturnDocument

from app.core.database import db
from app.models.user import UserInDB


class UserService:
    @staticmethod
    def insert_or_update_user(user: UserInDB):
        if hasattr(user, "id"):
            delattr(user, "id")
        finded = UserService.get_user(user)
        if finded is None:
            user.date_insert = datetime.utcnow()
            ret = db.user.insert_one(user.dict(by_alias=True))
        else:
            if hasattr(user, "date_insert"):
                delattr(user, "date_insert")
            if hasattr(user, "admin"):
                delattr(user, "admin")
            user.date_update = datetime.utcnow()
            user.disabled = finded.disabled
            ret = db.user.find_one_and_update(
                {"username": user.username},
                {"$set": user.dict(by_alias=True)},
                return_document=ReturnDocument.AFTER,
            )
        print(ret)
        return ret

    @staticmethod
    def get_user(user: UserInDB) -> UserInDB | None:
        ret = db.user.find_one({"username": user.username})
        if ret is not None:
            return UserInDB(**ret)
        else:
            return None
