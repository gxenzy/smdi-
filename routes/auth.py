from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from models.backup_code import BackupCode
from forms.backup_codes import GenerateBackupCodesForm
from extensions import db
import secrets
import string
from datetime import datetime
from models import User
from forms import LoginForm, RegistrationForm, UserCreationForm
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/backup-codes', methods=['GET', 'POST'])
@login_required
def backup_codes():
    form = GenerateBackupCodesForm()
    backup_codes = []
    
    if form.validate_on_submit():
        # Delete any unused existing codes
        BackupCode.query.filter_by(user_id=current_user.id, used=False).delete()
        
        # Generate new codes
        for _ in range(10):
            code = BackupCode(
                user_id=current_user.id,
                code=generate_backup_code()
            )
            db.session.add(code)
            backup_codes.append(code.code)
        
        db.session.commit()
        flash('New backup codes have been generated. Please save them in a secure location.', 'success')
    
    # Get existing codes for display
    existing_codes = BackupCode.query.filter_by(user_id=current_user.id).order_by(BackupCode.created_at.desc()).all()
    
    return render_template('auth/backup_codes.html', 
                           form=form, 
                           backup_codes=backup_codes,
                           existing_codes=existing_codes)

def generate_backup_code():
    """Generate a random 8-character backup code"""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))

@auth_bp.route('/use-backup-code/<code>')
@login_required
def use_backup_code(code):
    backup_code = BackupCode.query.filter_by(
        user_id=current_user.id,
        code=code,
        used=False
    ).first()
    
    if backup_code:
        backup_code.used = True
        backup_code.used_at = datetime.utcnow()
        db.session.commit()
        flash('Backup code accepted!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid or already used backup code.', 'danger')
        return redirect(url_for('auth.backup_codes'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Redirect to dashboard if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.identifier.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard after login
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form, title='Sign In')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the current user
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))  # Redirect to the login page

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Your registration logic here
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login after successful registration
    return render_template('register.html', form=form)  # Render the registration template

@auth_bp.route('/admin/create-user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:  # Check if the current user is an admin
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))  # Redirect to dashboard if not admin

    form = UserCreationForm()  # Instantiate your user creation form
    if form.validate_on_submit():
        # Create a new user with the provided details
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data  # Assign the specified role
        )
        new_user.set_password(form.password.data)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        flash('User  account created successfully!', 'success')
        return redirect(url_for('main.user_management'))  # Redirect to user management page

    return render_template('create_user.html', form=form)  # Render the user creation form template