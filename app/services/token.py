from datetime import datetime

from jose import jws
from pymongo.collection import ReturnDocument

from app.core import configuration
from app.core.database import db
from app.models.token import Token
from app.utils import current, PyObjectId

SECRET = configuration.APP_SECRET_TOKENS


class TokenService:
    """Service for TOKENS in database operations"""
    TABLE = db.token
    @classmethod
    def create(cls, item: Token) -> PyObjectId:
        """Create a new token in database

        Args:
            item (Token): Token to insert in database, required 'email'

        Returns:
            PyObjectId : Id of inserted token
        """
        item.date_insert = datetime.utcnow()
        item.disabled = False
        if hasattr(item, "date_update"):
            delattr(item, "date_update")
        if hasattr(item, "id"):
            delattr(item, "id")
        if hasattr(item, "username_update"):
            delattr(item, "username_update")
        payload = {"email": item.email, "current": current()}
        item.token = jws.sign(
            payload, SECRET, algorithm=configuration.APP_TOKEN_ALGORITHM
        )
        ret = cls.TABLE.insert_one(item.model_dump(by_alias=True))
        return ret.inserted_id

    @classmethod
    def get_by_id_and_email(cls, item: Token) -> Token | None:
        """
            Get a token by id and email in database

        Args:
            item (Token): Token to search in database, required 'id' and 'email'

        Returns:
            Token | None: Token found or None
        """
        find = cls.TABLE.find_one(
            {"_id": item.id, "email": item.email, "disabled": False}
        )
        if find is not None:
            return Token(**find)
        else:
            return None

    @classmethod
    def get_token(cls, token: str) -> Token | None:
        """Get a token object by token (JWS string) in database

        Args:
            token (str): Token to search in database (JWS string)

        Returns:
            Token | None: Token found or None
        """
        find = cls.TABLE.find_one({"disabled": False, "token": token})
        return find

    @classmethod
    def get(cls, email: str) -> list[Token]:
        """Get all tokens by email in database

        Args:
            email (str): Email to search in database

        Returns:
            list[Token]: List of tokens found
        """
        finds = cls.TABLE.find({"disabled": False, "email": email})
        items = []
        for find in finds:
            items.append(Token(**find))
        return items

    @classmethod
    def search(cls, item: Token) -> list[Token]:
        """Search tokens by email and token in database

        Args:
            item (Token): Token to search in database, required 'email' and 'token'

        Returns:
            list[Token]: List of tokens found in database
        """
        finds = cls.TABLE.find(
            {
                "$and": [
                    {"disabled": False},
                    {"email": item.email},
                    {"token": {"$regex": item.token}},
                ]
            }
        )
        tokens = []
        for find in finds:
            tokens.append(Token(**find))
        return tokens

    @classmethod
    def delete(cls, item: Token) -> None:
        """Delete a token in database

        Args:
            item (Token): Token to delete in database, required 'id' and 'email'
        """
        item.date_update = datetime.utcnow()
        ret = cls.TABLE.find_one_and_update(
            {"_id": item.id, "email": item.email, "disabled": False},
            {
                "$set": {
                    "disabled": True,
                    "date_update": item.date_update,
                    "username_update": item.username_update,
                }
            },
            return_document=ReturnDocument.AFTER,
        )
