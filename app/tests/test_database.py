from app.core.database import db


def test_database_test():
    assert db.name == "test"
