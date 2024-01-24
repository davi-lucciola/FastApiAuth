from users import get_user_by_username, users
from http import HTTPStatus
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime as dt, timedelta
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ---------------------------------------------------------------
# Schemas
class UserCredentials(BaseModel):
    username: str 
    password: str

# ---------------------------------------------------------------
# Bearer Security
# Informando que deve haver um header Authorization do tipo Bearer na requisição.
security = HTTPBearer()

# Chave secreta para encryptar e decryptar
ALGORITMO = 'HS256'
SUPER_SECRET_KEY = 'chave_muito_secreta'

# ---------------------------------------------------------------
# JWT Tokens
# Criando o Token
EXPIRATION_TIME = timedelta(hours=3)
def create_token(username: str, password: str) -> str:
    user_id, user = get_user_by_username(username)

    if user is None or user.get('password') != password:
        raise HTTPException(
            detail='Credênciais Inválidas.', 
            status_code=HTTPStatus.UNAUTHORIZED
        )

    initiated_at: dt = dt.utcnow()
    expires_on: dt = initiated_at + EXPIRATION_TIME
    token_payload = {
        'exp': expires_on, 
        'iat': initiated_at, 
        'user_id': user_id
    }

    return jwt.encode(token_payload, SUPER_SECRET_KEY, ALGORITMO)

# Validando o Token e Retornando o Usuario que gerou aquele token.
def authenticate_user(
    auth: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        token_payload: dict = jwt.decode(auth.credentials, SUPER_SECRET_KEY, ALGORITMO)
    except ExpiredSignatureError:
        raise HTTPException(
            detail='Token Expirado.', 
            status_code=HTTPStatus.UNAUTHORIZED
        )
    except JWTError:
        raise HTTPException(
            detail='Token inválido.', 
            status_code=HTTPStatus.UNAUTHORIZED
        )
    
    authenticated_user: dict = users.get(token_payload.get('user_id'))
    authenticated_user.pop('password')
    return authenticated_user
