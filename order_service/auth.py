from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://auth_service:8002/login")
SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-secreta")
ALGORITHM = "HS256"


def verifica_usuario(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=4401, detail="Token inválido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
