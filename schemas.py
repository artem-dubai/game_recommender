from pydantic import BaseModel


class GameCreate(BaseModel):
    title: str
    genres: str
    platform: str
    price: float
    rating: float
    playtime: int
    age_rating: int = 18
    region: str = "RU"


class GameResponse(GameCreate):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    favorite_genres: str
    preferred_platform: str
    max_price: float
    max_playtime: int = 100
    max_age_rating: int = 18
    region: str = "RU"


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True