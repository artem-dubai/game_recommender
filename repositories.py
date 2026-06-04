from sqlalchemy.orm import Session
from . import models, schemas


def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_games(db: Session):
    return db.query(models.Game).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.UserProfile(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(
        models.UserProfile.id == user_id
    ).first()