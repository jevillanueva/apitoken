from datetime import datetime

from jose import jws
from pymongo.collection import ReturnDocument

from app.core import configuration
from app.core.database import db
from app.models.token import Token
from app.utils.currentmillis import current

SECRET = configuration.APP_SECRET_TOKENS


class TokenService:
    @staticmethod
    def create(item: Token):
        item.date_insert = datetime.utcnow()
        item.disabled = False
        if hasattr(item, "date_update"):
            delattr(item, "date_update")
        if hasattr(item, "id"):
            delattr(item, "id")
        if hasattr(item, "username_update"):
            delattr(item, "username_update")
        payload = {"username": item.username, "current": current()}
        item.token = jws.sign(
            payload, SECRET, algorithm=configuration.APP_TOKEN_ALGORITHM
        )
        ret = db.token.insert_one(item.dict(by_alias=True))
        return ret

    @staticmethod
    def get_by_id_and_user(item: Token):
        finded = db.token.find_one(
            {"_id": item.id, "username": item.username, "disabled": False}
        )
        if finded is not None:
            return Token(**finded)
        else:
            return None

    @staticmethod
    def get_token(item: Token):
        finded = db.token.find_one({"disabled": False, "token": item.token})
        if finded is None:
            return None
        else:
            return finded

    @staticmethod
    def get(username: str):
        finded = db.token.find({"disabled": False, "username": username})
        items = []
        for find in finded:
            items.append(Token(**find))
        return items

    @staticmethod
    def search(item: Token):
        finded = db.token.find(
            {
                "$and": [
                    {"disabled": False},
                    {"username": item.username},
                    {"token": {"$regex": item.token}},
                ]
            }
        )
        tokens = []
        for find in finded:
            tokens.append(Token(**find))
        return tokens

    @staticmethod
    def delete(item: Token):
        item.date_update = datetime.utcnow()
        ret = db.token.find_one_and_update(
            {"_id": item.id, "username": item.username, "disabled": False},
            {
                "$set": {
                    "disabled": True,
                    "date_update": item.date_update,
                    "username_update": item.username_update,
                }
            },
            return_document=ReturnDocument.AFTER,
        )
        return ret
