from bcrypt import checkpw, hashpw, gensalt
def hash(pwd: str) -> str:
    return hashpw(pwd.encode(), gensalt())

def is_correct_pwd(pwd: str, hashed_pwd):
    return checkpw(pwd.encode, hashed_pwd)