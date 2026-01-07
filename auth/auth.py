from passlib.context import CryptContext
from database.db import get_session
from database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate(username, password):
    db = get_session()
    user = db.query(User).filter_by(username=username).first()
    db.close()

    if user and pwd_context.verify(password, user.password):
        return user
    return None