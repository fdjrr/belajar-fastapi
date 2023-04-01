import os
from datetime import datetime, timedelta
from typing import Annotated

from dotenv import load_dotenv
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.sql import text

from config.database import conn
from middleware.auth_bearer import JWTBearer
from middleware.auth_handler import decodeJWT
from models.users import UsersModel
from schemas.user import LoginSchema

load_dotenv()

user = APIRouter()
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']


@user.post('/user/login', description='Generate access token')
async def generate_access_token(login: LoginSchema):
  query = UsersModel.select().where(UsersModel.c.email == login.email)
  user = conn.execute(query).fetchone()
  if (user is None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not found')

  password_verify = password_context.verify(login.password, user.password)
  if (not password_verify):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Incorrect password')

  payload = {
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    'user': {
      'id': user.id,
      'email': user.email,
      'employee_id': user.employee_id,
      'role_id': user.role_id,
      'user_status_id': user.user_status_id,
    }
  }
  token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
  return {
    'access_token': token,
    'token_type': 'bearer'
  }


@user.get('/user/info', dependencies=[Depends(JWTBearer())], description='User information')
async def get_user(access_token: Annotated[str, Depends(oauth2_scheme)]):
  data = decodeJWT(access_token)
  employee_id = data['user']['employee_id']

  query = text("SELECT * FROM employees WHERE id =:x")
  params = query.bindparams(x=employee_id)
  employee = conn.execute(params).fetchone()
  print(employee.first_name)

  return {'status': True}
