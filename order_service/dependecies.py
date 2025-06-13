# order_service/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://auth_service:8002/login")

SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS256"


class TokenData(BaseModel):
    sub: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Tokén inálido")
        return user_id
    except (JWTError, ValidationError):
        raise HTTPException(
                status_code=401,
                detail="Token inválido ou expirado")