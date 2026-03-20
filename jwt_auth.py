import jwt 
from datetime import datetime, timedelta

SECRET_KEY = "secret-a8d93b5c1f0e4ce9f2a1c4d5e"
ALGORITHM = "HS256"

def create_token(username: str):
    expire = datetime.now() + timedelta(minutes=30)
    payload = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )
    return payload