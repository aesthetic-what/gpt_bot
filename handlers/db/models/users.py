from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from handlers.db.db_core import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    tg_id: Mapped[int]
    role: Mapped[str] = mapped_column(default='user')    
class Content(Base):
    __tablename__ = "content"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    