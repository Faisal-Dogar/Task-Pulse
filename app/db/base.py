from sqlalchemy.orm import DeclarativeBase  

class Base(DeclarativeBase):
    """
    Sub models is Base class se inherit karenge.
    Alembic migrations bhi isi metadata ko inspect karti hain.
    """
    pass