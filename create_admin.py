import argparse
from app import create_app
from extensions import db
from models.user import User

def validate_password(password):
    """Validate password meets minimum requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""

def create_admin_user(force=False, password=None):
    """Create admin user with optional force recreation."""
    app = create_app()
    with app.app_context():
        try:
            # Check if admin already exists
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                if not force:
                    print("Admin user already exists! Use --force to recreate.")
                    return False
                else:
                    # Delete existing admin
                    db.session.delete(admin)
                    db.session.commit()
                    print("Existing admin user deleted.")

            # Create new admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            
            # Use provided password or default
            admin_password = password or 'Admin123'
            
            # Validate password
            is_valid, message = validate_password(admin_password)
            if not is_valid:
                print(f"Error: {message}")
                return False
                
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created successfully!")
            print("Please change the password immediately after first login.")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create admin user')
    parser.add_argument('--force', action='store_true', 
                      help='Force recreate admin user if exists')
    parser.add_argument('--password', type=str,
                      help='Set specific password for admin user')
    args = parser.parse_args()
    
    success = create_admin_user(force=args.force, password=args.password)
    if success:
        print("\nAdmin user credentials:")
        print("Username: admin")
        print("Email: admin@example.com")
        print(f"Password: {args.password if args.password else 'Change_me_immediately!'}")
        print("\nPlease change this password after first login!")
    else:
        print("\nFailed to create admin user. Please check the errors above.")