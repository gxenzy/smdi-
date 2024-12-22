# In routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from forms.profile import ProfileForm
from models.user import User
from models.electrical_system import ElectricalSystem
from models.compliance_assessment import ComplianceAssessment
from models.energy_audit import EnergyAudit
from models.evaluation import Evaluation
from models.activity_log import ActivityLog
from extensions import db

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    user_count = User.query.count()
    electrical_system_count = ElectricalSystem.query.count()
    compliance_count = ComplianceAssessment.query.count()
    energy_audit_count = EnergyAudit.query.count()
    evaluation_count = Evaluation.query.count()

    dashboard_items = [
        {
            'title': 'Total Users',
            'description': f'{user_count} members have joined the website.',
            'url': url_for('main.user_management'),
            'button_text': 'Manage Users',
            'icon': 'fas fa-users'
        },
        {
            'title': 'Electrical Systems',
            'description': f'{electrical_system_count} electrical systems modeled.',
            'url': url_for('main.electrical_system'),
            'button_text': 'Access System',
            'icon': 'fas fa-bolt'
        },
        {
            'title': 'Compliance Assessments',
            'description': f'{compliance_count} compliance assessments completed.',
            'url': url_for('main.compliance'),
            'button_text': 'Run Assessment',
            'icon': 'fas fa-clipboard-check'
        },
        {
            'title': 'Energy Audit Tools',
            'description': f'{energy_audit_count} energy audits conducted.',
            'url': url_for('main.energy_audit'),
            'button_text': 'Launch Tool',
            'icon': 'fas fa-chart-line'
        },
        {
            'title': 'Testing Results',
            'description': 'View energy audit tool testing results.',
            'url': url_for('main.testing_results'),
            'button_text': 'View Results',
            'icon': 'fas fa-clipboard-list'
        },
        {
            'title': 'TAM Evaluations',
            'description': f'{evaluation_count} TAM evaluations completed.',
            'url': url_for('main.tam_evaluation'),
            'button_text': 'View Evaluation',
            'icon': 'fas fa-chart-bar'
        },
    ]

    return render_template('dashboard.html', 
                           user_count=user_count, 
                           electrical_system_count=electrical_system_count,
                           compliance_count=compliance_count,
                           energy_audit_count=energy_audit_count,
                           evaluation_count=evaluation_count,
                           dashboard_items=dashboard_items)

@main.route('/user-management')
@login_required
def user_management():
    users = User.query.all()
    return render_template('user_management.html', users=users)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()  # Create an instance of the ProfileForm

    if form.validate_on_submit():  # Check if the form is submitted and valid
        # Update the current user's information
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.bio = form.bio.data
        
        db.session.commit()  # Save changes to the database
        flash('Profile updated successfully!', 'success')  # Flash a success message
        return redirect(url_for('main.profile'))  # Redirect to the profile page

    # Pre-fill the form with the current user's data
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone.data = current_user.phone
    form.bio.data = current_user.bio

    return render_template('profile.html', form=form)

@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main.route('/activity-log')
@login_required
def activity_log():
    return render_template('activity_log.html')

@main.route('/compliance')
@login_required
def compliance():
    return render_template('compliance.html')

@main.route('/layout-3d')
@login_required
def layout_3d():
    return render_template('layout_3d.html')

@main.route('/electrical-system')
@login_required
def electrical_system():
    return render_template('electrical_system.html')

@main.route('/energy-audit')
@login_required
def energy_audit():
    return render_template('energy_audit.html')

@main.route('/testing-results')
@login_required
def testing_results():
    return render_template('testing_results.html')

@main.route('/tam-evaluation')
@login_required
def tam_evaluation():
    return render_template('tam_evaluation.html')

@main.route('/audit-tool')
@login_required
def audit_tool():
    return render_template('audit_tool.html')
