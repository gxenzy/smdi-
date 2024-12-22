import os
from app import create_app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        print("Starting database initialization...")
        try:
            # Ensure the database connection is working
            db.engine.connect()
            # Drop all tables and recreate them
            db.drop_all()
            print("Dropped existing tables")
            db.create_all()
            print("Created new tables")
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # Get admin password from environment variable or use secure default
                admin_password = os.getenv('ADMIN_PASSWORD', 'Change_me_immediately!')
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin',  # Ensure the role is set
                    avatar_url='admin.jpg',
                    first_name='Admin',
                    last_name='User '
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
                print("Please change the admin password immediately!")
            else:
                print("Admin user already exists!")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    success = init_db()
    if not success:
        print("Database initialization failed!")