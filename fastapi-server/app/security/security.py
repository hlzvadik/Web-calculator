import jwt
import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
import os
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass

def hash_password(password: str):
    hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    return hash_password.decode("utf-8")

def verify_password(password: str, hash_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))

