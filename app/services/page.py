from datetime import datetime
from typing import List

from pymongo.collection import ReturnDocument

from app.core.database import db
from app.models.page import Page, PageInDB
from app.utils.mongo_validator import PyObjectId


class PageService:
    TABLE = db.pages

    @classmethod
    def insert(cls, item: PageInDB) -> Page | None:
        item.date_insert = datetime.utcnow()
        item.disabled = False
        if hasattr(item, "date_update"):
            delattr(item, "date_update")
        if hasattr(item, "id"):
            delattr(item, "id")
        if hasattr(item, "username_update"):
            delattr(item, "username_update")

        ret = cls.get_by_slug(item.slug)
        if ret is None:
            inserted = cls.TABLE.insert_one(item.dict(by_alias=True))
            ret = cls.get(PyObjectId(inserted.inserted_id))
            return ret
        else:
            return None

    @classmethod
    def update(cls, item: PageInDB) -> Page | None:
        if hasattr(item, "date_insert"):
            delattr(item, "date_insert")
        if hasattr(item, "username_insert"):
            delattr(item, "username_insert")
        if hasattr(item, "disabled"):
            delattr(item, "disabled")
        item.date_update = datetime.utcnow()
        ret = cls.get_by_slug(item.slug)
        if ret is None or item.id == ret.id:
            ret = cls.TABLE.find_one_and_update(
                        {"_id": item.id, "disabled": False},
                        {"$set": item.dict(by_alias=True)},
                        return_document=ReturnDocument.AFTER,
                    )
            if ret is not None:
                return Page(**ret)
            else:
                return None
        else:
            return None

        

    @classmethod
    def delete(cls, item: PageInDB) -> Page | None:
        item.date_update = datetime.utcnow()
        ret = cls.TABLE.find_one_and_update(
            {"_id": item.id, "disabled": False},
            {
                "$set": {
                    "disabled": True,
                    "date_update": item.date_update,
                    "username_update": item.username_update,
                }
            },
            return_document=ReturnDocument.AFTER,
        )
        if ret is not None:
            return Page(**ret)
        else:
            return None

    @classmethod
    def get(cls, id: PyObjectId) -> Page | None:
        search = cls.TABLE.find_one({"_id": id, "disabled": False})
        if search is not None:
            return Page(**search)
        else:
            return None

    @classmethod
    def list(cls, page_number: int = 0, n_per_page: int = 100) -> List[Page]:
        search = (
            cls.TABLE.find({"disabled": False})
            .skip(((page_number - 1) * n_per_page) if page_number > 0 else 0)
            .limit(n_per_page)
        )
        items = []
        for find in search:
            items.append(Page(**find))
        return items

    @classmethod
    def search(cls, q: str, page_number: int = 0, n_per_page: int = 100) -> List[Page]:
        search = (
            cls.TABLE.find(
                {
                    "$and": [
                        {"disabled": False},
                        {
                            "$or": [
                                {
                                    "slug": {
                                        "$regex": q,
                                        "$options": "i",
                                    }
                                },
                                {"title": {"$regex": q, "$options": "i"}},
                            ]
                        },
                    ]
                }
            )
            .skip(((page_number - 1) * n_per_page) if page_number > 0 else 0)
            .limit(n_per_page)
        )
        items = []
        for find in search:
            items.append(Page(**find))
        return items

    @classmethod
    def get_by_slug(cls, slug: str) -> Page | None:
        search = cls.TABLE.find_one({"slug": slug, "disabled": False})
        if search is not None:
            return Page(**search)
        else:
            return None