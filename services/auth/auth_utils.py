from bcrypt import checkpw, hashpw, gensalt


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        return False


def getPasswordHash(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')