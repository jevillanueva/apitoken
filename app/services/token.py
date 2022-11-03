
from app.core.database import db
from app.models.token import Token


class TokenService:
    @staticmethod
    def get_token(item: Token):
        finded = db.token.find_one({"disabled": False, "token": item.token})
        if finded is None:
            return None
        else:
            return finded