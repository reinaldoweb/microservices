from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas import TokenData
import os

SECRETE_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS2256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verifica_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")