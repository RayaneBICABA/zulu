import logging
import pytest
from unittest.mock import patch
from app import create_app
from app.extensions import db as _db

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db(app):
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()

@pytest.fixture(autouse=True)
def mock_smtp():
    with patch("app.services.email_service._send_smtp") as mock:
        yield mock
