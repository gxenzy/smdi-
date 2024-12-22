from app import app, db
from models.user import User

def create_test_user():
    with app.app_context():
        # Check if test user already exists
        if not User.query.filter_by(username='testuser').first():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print("Test user created successfully")
            print("Username: testuser")
            print("Password: password123")
        else:
            print("Test user already exists")

if __name__ == '__main__':
    create_test_user()
