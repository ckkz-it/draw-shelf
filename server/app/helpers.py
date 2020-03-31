import bcrypt
from uuid import uuid4


def stringified_uuid():
    return str(uuid4())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))
