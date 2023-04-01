import os
import time

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()


SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']


def decodeJWT(token: str) -> dict:
  try:
    data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return data if (data["exp"] >= time.time()) else None
  except JWTError as e:
    return {}
