import os

class Config:
    """Base configuration class."""
    
    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sdmisql:cXg4uIEMAUQ2zy5O@127.0.0.1/smdi'
    
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', '3Wft0F67nxRuAb5g')

    # Optional: Add configurations for other services if needed
    # Example: Mail server configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')  # Your mail server
    MAIL_PORT = os.getenv('MAIL_PORT', 587)  # Mail server port
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)  # Use TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Mail server username
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Mail server password
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')  # Default sender email

    # Optional: Other configurations can be added here