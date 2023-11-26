from datetime import datetime
from typing import List

from pymongo.collection import ReturnDocument

from app.core.database import db
from app.models.page import Page, PageInDB
from app.utils import PyObjectId


class PageService:
    """Service for PAGES in database operations"""

    TABLE = db.pages

    @classmethod
    def insert(cls, item: PageInDB) -> Page | None:
        """Insert a new page in database if slug not exists

        Args:
            item (PageInDB): Page to insert in database required 'slug'

        Returns:
            Page | None: Page inserted or None if slug exists
        """
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
        """Update a page in database using id and slug to validate

        Args:
            item (PageInDB): Page to update in database required 'id' and 'slug'

        Returns:
            Page | None: Page updated or None if slug exists in other page or not found
        """
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
                {"$set": item.model_dump(by_alias=True)},
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
        """Page delete in database using the id to validate delete

        Args:
            item (PageInDB): Page to delete in database required 'id'

        Returns:
            Page | None: Page deleted or None if not found or already deleted
        """
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
        """Get a page from database by id

        Args:
            id (PyObjectId): Id of page to find

        Returns:
            Page | None: Page found or None if not found
        """
        search = cls.TABLE.find_one({"_id": id, "disabled": False})
        if search is not None:
            return Page(**search)
        else:
            return None

    @classmethod
    def list(cls, page_number: int = 0, n_per_page: int = 100) -> List[Page]:
        """List all pages in database using pagination

        Args:
            page_number (int, optional): Page number to list. Defaults to 0.
            n_per_page (int, optional): Number of items per page. Defaults to 100.

        Returns:
            List[Page]: List of pages found in database
        """
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
        """Search pages in database using query and pagination

        Args:
            q (str): Query to search in database
            page_number (int, optional): Page number to list. Defaults to 0.
            n_per_page (int, optional): Number of items per page. Defaults to 100.

        Returns:
            List[Page]: List of pages found in database
        """
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
        """Get a page from database by slug

        Args:
            slug (str): Slug of page to find in database

        Returns:
            Page | None: Page found or None if not found
        """
        search = cls.TABLE.find_one({"slug": slug, "disabled": False})
        if search is not None:
            return Page(**search)
        else:
            return None
