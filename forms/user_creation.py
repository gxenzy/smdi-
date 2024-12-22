# forms/user_creation.py (create this file if it doesn't exist)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('user', 'User '), ('admin', 'Admin'), ('moderator', 'Moderator')], validators=[DataRequired()])
    submit = SubmitField('Create User')