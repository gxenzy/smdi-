import pytest
from models.user import User
from extensions import db

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and password fields are defined correctly
    """
    user = User(
        username='test_user',
        email='test@test.com'
    )
    user.set_password('test_password')
    assert user.username == 'test_user'
    assert user.email == 'test@test.com'
    assert user.check_password('test_password')
