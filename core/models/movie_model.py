from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title_es: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
