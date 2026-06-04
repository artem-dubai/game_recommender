from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    playtime = Column(Integer, nullable=False)
    age_rating = Column(Integer, nullable=False, default=18)
    region = Column(String, nullable=False, default="RU")


class UserProfile(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    favorite_genres = Column(String, nullable=False)
    preferred_platform = Column(String, nullable=False)
    max_price = Column(Float, nullable=False)
    max_playtime = Column(Integer, nullable=False, default=100)
    max_age_rating = Column(Integer, nullable=False, default=18)
    region = Column(String, nullable=False, default="RU")