from passlib.hash import bcrypt
from database.db import get_session
from database.models import User

def authenticate(username, password):
    db = get_session()
    user = db.query(User).filter_by(username=username).first()
    if user and bcrypt.verify(password, user.password):
        return user
    return None

def require_role(user, allowed):
    if user.role not in allowed:
        raise PermissionError
