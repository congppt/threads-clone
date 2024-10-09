import bcrypt


def hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())