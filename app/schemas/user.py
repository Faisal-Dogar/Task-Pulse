from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Agar email-validator installed ho to EmailStr use karein, warna str use karein (taake crash na ho)
try:
    import email_validator  # noqa: F401
    from pydantic import EmailStr
except ImportError:
    EmailStr = str

from app.models.user import UserRole


# 1. Base Schema: Common fields jo har user ke paas hote hain
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.DEVELOPER
    is_active: bool = True


# 2. Create Schema: Jab naya user register hota hai (password lazmi hai)
class UserCreate(UserBase):
    password: str


# 3. Update Schema: Jab profile update karni ho (tamam fields optional hain)
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


# 4. Response Schema: Jab API se user data wapas bhejna ho (password return nahi hota)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    # SQLAlchemy model ko automatically Pydantic schema me convert karta hai
    model_config = ConfigDict(from_attributes=True)
