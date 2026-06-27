import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
swagger = Swagger()
limiter = Limiter(
	key_func=get_remote_address,
	default_limits=[],
	storage_uri=os.getenv("LIMITER_STORAGE_URL") or "memory://",
	in_memory_fallback_enabled=True,
	swallow_errors=True,
)
