import os
import logging
import secrets
import string
from collections import deque
from ipaddress import ip_address, IPv4Address, IPv6Address
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session, current_app
from routes.main import main as main_blueprint
from routes.auth import auth_bp
from extensions import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from dotenv import load_dotenv
from urllib.parse import urlparse
from forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from models import User, ActivityLog, BackupCode, ElectricalSystem
from models.compliance_assessment import ComplianceAssessment
from models.energy_audit import EnergyAudit
from models.evaluation import Evaluation
from models.user import User
from config import Config
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException
from wtforms.validators import Email, Length
from werkzeug.utils import secure_filename


load_dotenv()

# Initialize extensions
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
mysql = MySQL()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app
    mysql.init_app(app)  # Initialize MySQL with the app
    login_manager.init_app(app)  # Initialize Flask-Login with the app
    csrf.init_app(app)  # Initialize CSRF protection with the app
    mail.init_app(app)  # Initialize Flask-Mail with the app
    login_manager.login_view = 'auth.login'
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def get_client_ip(request):
        """Retrieve the client's IP address."""
        if 'X-Forwarded-For' in request.headers:
            ip_parts = request.headers['X-Forwarded-For'].split(',')
            for ip_part in ip_parts:
                ip_part = ip_part.strip()
                if ip_part:
                    try:
                        return str(ip_address(ip_part))
                    except ValueError:
                        continue
        if 'X-Real-IP' in request.headers:
            try:
                return str(ip_address(request.headers['X-Real-IP'].strip()))
            except ValueError:
                pass
        return request.remote_addr

    @app.route('/')
    def index():
        return redirect(url_for('main.dashboard')) if current_user.is_authenticated else redirect(url_for('auth.login'))

    @app.route('/users', methods=['GET'])
    @login_required
    def get_users():
        """Fetch all users from the database."""
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        cur.close()
        return jsonify([{'id': user[0], 'username': user[1], 'email': user[2]} for user in users])

    def get_user_count():
        return User.query.count()

    def get_electrical_system_count():
        return ElectricalSystem.query.count()
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        try:
            # Fetch data for the dashboard
            user_count = get_user_count()
            electrical_system_count = get_electrical_system_count()
            compliance_count = ComplianceAssessment.query.count()  # Example for compliance count
            energy_audit_count = EnergyAudit.query.count()  # Example for energy audit count
            evaluation_count = Evaluation.query.count()  # Example for evaluation count
            error_message = None
        except Exception as e:
            error_message = str(e)  # Capture the error message
            user_count = 0
            electrical_system_count = 0
            compliance_count = 0
            energy_audit_count = 0
            evaluation_count = 0

        return render_template('dashboard.html', 
                               user_count=user_count, 
                               electrical_system_count=electrical_system_count, 
                               compliance_count=compliance_count, 
                               energy_audit_count=energy_audit_count, 
                               evaluation_count=evaluation_count, 
                               error_message=error_message)

    @app.route('/admin/create-user', methods=['GET', 'POST'])
    @login_required
    def create_user():
        """Admin route to create a new user."""
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Check if the username already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('create_user'))

            # Validate email format
            if not Email()(email):
                flash('Invalid email address', 'danger')
                return redirect(url_for('create_user'))

            # Create the new user
            new_user = User(username=username, email=email)
            new_user.set_password(password)  # Hash the password
            db.session.add(new_user)
            db.session.commit()
            flash('User  created successfully!', 'success')
            return redirect(url_for('dashboard'))

        return render_template('create_user.html')

    @app.route('/make-admin/<int:user_id>', methods=['POST'])
    @login_required
    def make_admin(user_id):
        """Make a user an admin."""
        if not current_user.is_admin:
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('dashboard'))
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            flash(f'User  {user.username} has been granted admin privileges.', 'success')
        else:
            flash('User  not found.', 'danger')
            return redirect(url_for('user_management'))

    @app.route('/compliance')
    @login_required
    def compliance():
        return render_template('compliance.html')

    @app.route('/layout-3d')
    @login_required
    def layout_3d():
        return render_template('layout_3d.html', title='3D Layout')

    @app.route('/electrical-system', methods=['GET'])
    @login_required
    def electrical_system():
        return render_template('electrical_system.html', title='Electrical System')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/user-management')
    @login_required
    def user_management():
        users = User.query.all()
        return render_template('user_management.html', users=users)

    @app.route('/energy-audit')
    @login_required
    def energy_audit():
        return render_template('energy_audit.html')

    @app.route('/testing-results')
    @login_required
    def testing_results():
        return render_template('testing_results.html')

    @app.route('/tam-evaluation')
    @login_required
    def tam_evaluation():
        return render_template('tam_evaluation.html')

    @app.route('/audit-tool')
    @login_required
    def audit_tool():
        return render_template('audit_tool.html')

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        if request.method == 'POST':
            current_user.theme_preference = request.form.get('theme_preference')
            current_user.notification_enabled = 'notification_enabled' in request.form
            db.session.commit()
            flash('Settings updated successfully', 'success')
            return redirect(url_for('settings'))
        return render_template('settings.html')

    @app.route('/activity-log')
    @login_required
    def activity_log():
        return render_template('activity_log.html')

    @app.route('/backup-codes', methods=['GET', 'POST'])
    @login_required
    def backup_codes():
        if request.method == 'POST':
            BackupCode.query.filter_by(user_id=current_user.id, used=False).delete()
            backup_codes = []
            for _ in range(10):
                code = BackupCode(
                    user_id=current_user.id,
                    code=''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                )
                db.session.add(code)
                backup_codes.append(code.code)
            db.session.commit()
            flash('New backup codes have been generated. Please save them in a secure location.', 'success')
            return render_template('backup_codes.html', backup_codes=backup_codes)

        existing_codes = BackupCode.query.filter_by(user_id=current_user.id).order_by(BackupCode.created_at.desc()).all()
        return render_template('backup_codes.html', existing_codes=existing_codes)

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()  # Create an instance of the ProfileForm
        
        if request.method == 'POST':
            # Log the received form data for debugging
            app.logger.debug(f'Received form data: {request.form}')

            try:
                # Handle avatar upload
                if 'avatar' in request.files:
                    avatar = request.files['avatar']
                    if avatar and allowed_file(avatar.filename):
                        filename = secure_filename(avatar.filename)
                        avatar_path = os.path.join(current_app.root_path, 'static', 'avatars', filename)
                        avatar.save(avatar_path)
                        current_user.avatar_url = filename  # Update the user's avatar URL
            
                # Update other profile fields
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.phone = form.phone.data
                current_user.bio = form.bio.data
                current_user.notification_enabled = 'notification_enabled' in request.form
                
                # Log the profile update activity
                log = ActivityLog(
                    user_id=current_user.id,
                    action='profile_update',
                    ip_address=get_client_ip(request)
                )
                db.session.add(log)
                db.session.commit()  # Save changes to the database
                
                flash('Profile updated successfully', 'success')
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Profile update error: {str(e)}')
                flash('Error updating profile. Please try again.', 'error')
            
            return redirect(url_for('profile'))
        
        # Render the profile template and pass the form to it
        return render_template('profile.html', form=form, ActivityLog=ActivityLog)

    @app.route('/add-user', methods=['POST'])
    @login_required
    def add_user():
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(url_for('user_management'))
                
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('User  added successfully', 'success')
            return redirect(url_for('user_management'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding user: {str(e)}', 'error')
            return redirect(url_for('user_management'))

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error=str(error)), 404

    @app.errorhandler(500) 
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html', error="Internal Server Error"), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        app.logger.error(f'Unhandled Exception: {str(e)}')
        db.session.rollback()
        return render_template('error.html', error="An unexpected error occurred. Please try again later."), 500

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:  # Prevent login if already authenticated
            return redirect(url_for('dashboard'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.identifier.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('dashboard'))  # Redirect explicitly to avoid overlaps
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('login.html', form=form, title='Sign In')

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.get_reset_token()
                msg = Message('Password Reset Request',
                              sender='noreply@yourdomain.com',
                              recipients=[user.email])
                msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
                mail.send(msg)
                flash('Check your email for instructions to reset your password.', 'info')
                return redirect(url_for('login'))
            else:
                flash('No account found with that email address.', 'error')
        
        return render_template('forgot_password.html', form=form)

    @app.route('/reset-password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        user = User.query.filter_by(reset_token=token).first()
        if not user or not user.verify_reset_token(token):
            flash('Invalid or expired reset token.', 'error')
            return redirect(url_for('forgot_password'))
        
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            user.clear_reset_token()
            db.session.commit()
            flash('Your password has been reset.', 'success')
            return redirect(url_for('login'))
            
        return render_template('reset_password.html', form=form)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)