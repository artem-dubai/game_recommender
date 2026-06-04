import csv
import json
import time
from .exceptions import (
    RecommendationError,
    recommendation_exception_handler,
)
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas, repositories
from .recommender import build_recommendations, fallback_recommendations
from .filters import filter_games
from .explanation import generate_explanation
from .logger_config import logger

import logging

logger = logging.getLogger("game_recommender")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ПМ ИПВ",
    description="Программный модуль интеллектуального подбора видеоигр",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "ПМ ИПВ работает"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/games", response_model=schemas.GameResponse)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    return repositories.create_game(db, game)


@app.get("/games", response_model=list[schemas.GameResponse])
def get_games(db: Session = Depends(get_db)):
    return repositories.get_games(db)


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return repositories.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = repositories.get_user(db, user_id)

    if user is None:
        logger.warning(f"Пользователь {user_id} не найден")

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    return user


@app.post("/recommend/{user_id}")
def recommend_games(user_id: int, db: Session = Depends(get_db)):
    start_time = time.perf_counter()

    logger.info(f"Запрос рекомендаций для пользователя {user_id}")

    user = repositories.get_user(db, user_id)

    if user is None:
        logger.warning(f"Пользователь {user_id} не найден")

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    logger.info(f"Пользователь найден: {user.username}")

    games = repositories.get_games(db)

    if not games:
        logger.warning("Каталог игр пуст")

        raise HTTPException(
            status_code=404,
            detail="Каталог игр пуст",
        )

    logger.info(f"Количество игр в каталоге: {len(games)}")

    try:
        recommendations = build_recommendations(user, games)

    except Exception as error:
        logger.error(
            f"Ошибка генерации рекомендаций: {str(error)}"
        )

        raise RecommendationError(
            "Ошибка работы рекомендательной системы"
        )
    
    filtered_recommendations = filter_games(user, recommendations)

    if not filtered_recommendations:
        logger.warning(
            "Рекомендации не найдены. Используется fallback-логика."
        )
        filtered_recommendations = fallback_recommendations(games)

    result = []

    for game, score in filtered_recommendations:
        result.append(
            {
                "game_id": game.id,
                "title": game.title,
                "genres": game.genres,
                "platform": game.platform,
                "price": game.price,
                "rating": game.rating,
                "playtime": game.playtime,
                "age_rating": game.age_rating,
                "region": game.region,
                "similarity": round(float(score), 4),
                "explanation": generate_explanation(user, game),
            }
        )

    end_time = time.perf_counter()
    response_time = round(end_time - start_time, 4)

    total_games = len(games)
    filtered_games = len(result)
    rejected_games = total_games - filtered_games

    logger.info(
        f"Сформировано {filtered_games} рекомендаций "
        f"за {response_time} сек"
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "recommendations_count": filtered_games,
        "total_games_checked": total_games,
        "rejected_games_count": rejected_games,
        "response_time_seconds": response_time,
        "algorithm": "TF-IDF + cosine similarity + context filtering",
        "recommendations": result,
    }


@app.get("/export/json/{user_id}")
def export_recommendations_json(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = repositories.get_user(db, user_id)

    if user is None:
        logger.warning(f"Пользователь {user_id} не найден при JSON экспорте")

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    games = repositories.get_games(db)

    if not games:
        logger.warning("Каталог игр пуст при JSON экспорте")

        raise HTTPException(
            status_code=404,
            detail="Каталог игр пуст",
        )

    recommendations = build_recommendations(user, games)
    filtered_recommendations = filter_games(user, recommendations)

    if not filtered_recommendations:
        filtered_recommendations = fallback_recommendations(games)

    result = []

    for game, score in filtered_recommendations:
        result.append(
            {
                "title": game.title,
                "genres": game.genres,
                "platform": game.platform,
                "price": game.price,
                "rating": game.rating,
                "playtime": game.playtime,
                "age_rating": game.age_rating,
                "region": game.region,
                "similarity": round(float(score), 4),
                "explanation": generate_explanation(user, game),
            }
        )

    filename = f"recommendations_user_{user_id}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=4,
        )

    logger.info(f"JSON экспорт создан: {filename}")

    return {
        "message": "JSON экспорт успешно создан",
        "file": filename,
    }


@app.get("/export/csv/{user_id}")
def export_recommendations_csv(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = repositories.get_user(db, user_id)

    if user is None:
        logger.warning(f"Пользователь {user_id} не найден при CSV экспорте")

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    games = repositories.get_games(db)

    if not games:
        logger.warning("Каталог игр пуст при CSV экспорте")

        raise HTTPException(
            status_code=404,
            detail="Каталог игр пуст",
        )

    recommendations = build_recommendations(user, games)
    filtered_recommendations = filter_games(user, recommendations)

    if not filtered_recommendations:
        filtered_recommendations = fallback_recommendations(games)

    filename = f"recommendations_user_{user_id}.csv"

    with open(
        filename,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "Title",
                "Genres",
                "Platform",
                "Price",
                "Rating",
                "Playtime",
                "Age rating",
                "Region",
                "Similarity",
                "Explanation",
            ]
        )

        for game, score in filtered_recommendations:
            writer.writerow(
                [
                    game.title,
                    game.genres,
                    game.platform,
                    game.price,
                    game.rating,
                    game.playtime,
                    game.age_rating,
                    game.region,
                    round(float(score), 4),
                    generate_explanation(user, game),
                ]
            )

    logger.info(f"CSV экспорт создан: {filename}")

    return {
        "message": "CSV экспорт успешно создан",
        "file": filename,
    }