from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole

# 1. OAuth2 scheme:
# Yeh Swagger UI me 'Authorize' button show karta hai
# aur request ke Authorization header se Bearer token extract karta hai
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


# 2. Dependency: Token verify karke logged-in user nikalna
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Har protected route ke liye check karta hai ke token valid hai ya nahi,
    aur database se authenticated user return karta hai.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Token decode karein
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Database se user fetch karein
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    # Check karein agar user active hai
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )

    return user


# 3. RBAC (Role-Based Access Control) Helper Class
class RoleChecker:
    """
    Yeh class check karti hai ke logged-in user ka role allowed roles me shamil hai ya nahi.
    Agar permission na ho to HTTP 403 Forbidden error throw karegi.
    """
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to perform this action"
            )
        return current_user


# Asani ke liye pre-defined shortcuts:
allow_admin_only = RoleChecker([UserRole.ADMIN])
allow_admin_or_manager = RoleChecker([UserRole.ADMIN, UserRole.MANAGER])
allow_all_authenticated = RoleChecker([UserRole.ADMIN, UserRole.MANAGER, UserRole.DEVELOPER])
