from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# 1. Password Hashing helper (Argon2 algorithm use karta hai jo modern aur bohot secure hai)
password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Login ke waqt check karta hai ke user ka enter kiya hua password
    database ke hashed password se match karta hai ya nahi.
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Register karte waqt user ke plain password ko secure hash banata hai
    taake database me plain password save na ho.
    """
    return password_hash.hash(password)


# 2. JWT Access Token Generator
def create_access_token(
    subject: Union[str, Any], 
    role: str,
    expires_delta: timedelta | None = None
) -> str:
    """
    User ID aur Role ko encode karke ek JWT (JSON Web Token) banata hai.
    Yeh token user ko login ke baad diya jata hai.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Token ke andar jo data save karna hai (payload)
    to_encode = {
        "sub": str(subject),      # User ID
        "role": role,             # User Role (admin / manager / developer)
        "exp": expire             # Token kab expire hoga
    }

    # Secret key aur algorithm ke zariye token sign karein
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
