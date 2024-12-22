from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models.backup_code import BackupCode
from forms.backup_codes import GenerateBackupCodesForm
from extensions import db
import secrets
import string
from datetime import datetime

bp = Blueprint('backup_codes', __name__)

def generate_backup_code():
    """Generate a random 8-character backup code"""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))

@bp.route('/backup-codes', methods=['GET', 'POST'])
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
    
    return render_template('backup_codes.html', 
                         form=form, 
                         backup_codes=backup_codes,
                         existing_codes=existing_codes)

@bp.route('/use-backup-code/<code>')
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
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid or already used backup code.', 'danger')
        return redirect(url_for('login'))
