from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas import Token
import os

SECRETE_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verifica_token(token: str = Depends(oauth2_scheme)) -> Token:
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return Token(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")