from .database import Base, engine, SessionLocal
from .models import Game, UserProfile

Base.metadata.create_all(bind=engine)

db = SessionLocal()

games = [
    Game(
        title="Cyberpunk 2077",
        genres="RPG Action Open-World Sci-Fi",
        platform="PC",
        price=1999,
        rating=9.1,
        playtime=40,
        age_rating=18,
        region="RU",
    ),
    Game(
        title="The Witcher 3",
        genres="RPG Fantasy Open-World Adventure",
        platform="PC",
        price=1499,
        rating=9.8,
        playtime=60,
        age_rating=18,
        region="RU",
    ),
    Game(
        title="Elden Ring",
        genres="RPG Souls-Like Fantasy Action",
        platform="PC",
        price=2499,
        rating=9.7,
        playtime=80,
        age_rating=18,
        region="RU",
    ),
    Game(
        title="FIFA 24",
        genres="Sports Football Multiplayer",
        platform="PS5",
        price=2999,
        rating=7.5,
        playtime=25,
        age_rating=3,
        region="EU",
    ),
    Game(
        title="God of War Ragnarok",
        genres="Action Adventure Mythology",
        platform="PS5",
        price=3499,
        rating=9.4,
        playtime=35,
        age_rating=18,
        region="EU",
    ),
    Game(
        title="Stardew Valley",
        genres="Simulation Farming Indie Relaxing",
        platform="PC",
        price=499,
        rating=9.3,
        playtime=70,
        age_rating=12,
        region="RU",
    ),
    Game(
        title="Hades",
        genres="Roguelike Action Indie Mythology",
        platform="PC",
        price=799,
        rating=9.5,
        playtime=30,
        age_rating=16,
        region="RU",
    ),
    Game(
        title="Forza Horizon 5",
        genres="Racing Open-World Cars",
        platform="PC",
        price=2499,
        rating=8.9,
        playtime=45,
        age_rating=3,
        region="RU",
    ),
    Game(
        title="Baldur's Gate 3",
        genres="RPG Turn-Based Fantasy Strategy",
        platform="PC",
        price=1999,
        rating=9.9,
        playtime=100,
        age_rating=18,
        region="RU",
    ),
    Game(
        title="Minecraft",
        genres="Sandbox Survival Creative Multiplayer",
        platform="PC",
        price=1200,
        rating=9.0,
        playtime=200,
        age_rating=7,
        region="RU",
    ),
]

user = UserProfile(
    username="ilya",
    favorite_genres="RPG Action Fantasy Open-World",
    preferred_platform="PC",
    max_price=2500,
    max_playtime=100,
    max_age_rating=18,
    region="RU",
)

db.add_all(games)
db.add(user)

db.commit()
db.close()

print("База данных успешно заполнена.")