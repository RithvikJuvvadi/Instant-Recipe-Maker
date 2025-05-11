from recipe.app import app

from models import db, User  # Corrected import path





# Create all the tables in the database
with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")
