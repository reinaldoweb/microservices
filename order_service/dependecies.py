from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

# Carrega as variáveis de ambiente do .env
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-padrao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Define o esquema de autenticação com OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """
    Valida e decodifica o token JWT recebido no cabeçalho Authorization (Bearer token).
    Retorna o user_id contido no token se for válido. Caso contrário, levanta um HTTP 401.
    """
    try:
        # Decodifica o token usando a chave e algoritmo definidos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Busca o valor associado à chave "sub" no payload do token
        user_id: str = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Token inválido: ID do usuário ausente"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )
