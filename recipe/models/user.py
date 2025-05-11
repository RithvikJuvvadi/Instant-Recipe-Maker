from . import db
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):  # Inherit from UserMixin
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Full Name
    dob = db.Column(db.Date, nullable=False)  # Date of Birth
    phone = db.Column(db.String(15), nullable=False)  # Phone Number
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email
    password_hash = db.Column(db.String(200), nullable=False)  # Password Hash

    def validate_name(self, name):
        if not name.isalpha():
            return False
        return True

    def validate_phone(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            return False
        return True

    def set_password(self, password):
        print(f"Setting password for user: {self.email}")  # Debug log
        self.password_hash = generate_password_hash(password)
        print("Password hash generated successfully")  # Debug log

    def check_password(self, password):
        print(f"Checking password for user: {self.email}")  # Debug log
        result = check_password_hash(self.password_hash, password)
        print(f"Password check result: {result}")  # Debug log
        return result

    @property
    def is_active(self):
        return True  # You can implement your own logic here if needed

    @property
    def is_authenticated(self):
        return True  # Always return True for authenticated users

    @property
    def is_anonymous(self):
        return False  # Always return False for authenticated users

    def get_id(self):
        return str(self.id)  # Return the unique identifier for the user

    def __repr__(self):
        return f"<User {self.name}>"

    # Other fields remain unchanged
