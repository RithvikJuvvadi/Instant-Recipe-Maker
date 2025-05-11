from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to avoid circular imports
from .user import User  
from .recipe import Recipe
