from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Film(Base):
    __tablename__ = "film"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)

    codes = relationship("Code", back_populates="code_film")
    dates = relationship("Date", back_populates="date_film")


class Code(Base):
    __tablename__ = "code"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("film.id"), nullable=False)
    code = Column(String, nullable=False)

    code_film = relationship("Film", back_populates="codes")


class Date(Base):
    __tablename__ = "date"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("film.id"), nullable=False)
    date = Column(DateTime, nullable=False)

    date_film = relationship("Film", back_populates="dates")


