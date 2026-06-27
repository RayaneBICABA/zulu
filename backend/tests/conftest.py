import logging
import pytest
from unittest.mock import patch
from app import create_app
from app.extensions import db as _db
from app.models.role import Role

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
def seed_default_roles(app):
    with app.app_context():
        for name, desc in [
            ("client", "Client — cherche des services"),
            ("artisan", "Artisan — prestataire de service"),
            ("admin", "Administrateur du systeme"),
        ]:
            if not Role.query.filter_by(name=name).first():
                role = Role(name=name, description=desc)
                _db.session.add(role)
        _db.session.commit()

@pytest.fixture(autouse=True)
def mock_smtp():
    with patch("app.services.email_service._send_smtp") as mock:
        yield mock
