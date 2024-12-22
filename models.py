from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Keep this for storing hashed password
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add this field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Security tracking
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    locked_until = db.Column(db.DateTime)
    
    # User preferences
    notification_enabled = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(20), default='light')
    role = db.Column(db.String(20), default='user')
    
    # Profile information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_url = db.Column(db.String(200), nullable=True)  # Nullable if not required
    first_name = db.Column(db.String(50), nullable=True)  # Nullable if not required
    last_name = db.Column(db.String(50), nullable=True)  # Nullable if not required
    phone = db.Column(db.String(20), nullable=True)  # Nullable if not required
    bio = db.Column(db.Text, nullable=True)  # Nullable if not required
    
    # Password reset
    reset_token = db.Column(db.String(100), unique=True, nullable=True)  # Nullable if not required
    reset_token_expiry = db.Column(db.DateTime, nullable=True)  # Nullable if not required

    def set_password(self, password):
        """Set the user's password to a hashed version."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)
    
    class ElectricalSystem(db.Model):
        __tablename__ = 'electrical_system'  # Ensure the table name matches
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        # Add other fields as necessary

        def __repr__(self):
            return f'<ElectricalSystem {self.name}>'
    
    class ComplianceAssessment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        status = db.Column(db.String(20), nullable=False)
    
    class EnergyAudit(db.Model):
        __tablename__ = 'energy_audit'  # Ensure the table name matches your SQL query
        id = db.Column(db.Integer, primary_key=True)
        result = db.Column(db.String(255), nullable=False)  # Adjust the size based on your needs

    class Evaluation(db.Model):
        __tablename__ = 'evaluation'  # Ensure the table name matches your SQL query
        id = db.Column(db.Integer, primary_key=True)
        user_acceptance = db.Column(db.Boolean, nullable=False)  # Adjust the data type as necessary

    db.create_all()
    
    