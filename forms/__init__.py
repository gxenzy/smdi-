# forms/__init__.py

from .auth import LoginForm, ForgotPasswordForm, ResetPasswordForm, RegistrationForm
from .backup_codes import GenerateBackupCodesForm
from .user_creation import UserCreationForm
from .profile import ProfileForm