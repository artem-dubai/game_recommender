def generate_explanation(user, game):
    explanation = []

    if user.preferred_platform == game.platform:
        explanation.append(f"доступно на платформе {game.platform}")

    if game.price <= user.max_price:
        explanation.append(f"цена {game.price} не превышает бюджет {user.max_price}")

    if game.playtime <= user.max_playtime:
        explanation.append(f"время прохождения {game.playtime} ч подходит под ограничение")

    if game.age_rating <= user.max_age_rating:
        explanation.append(f"возрастной рейтинг {game.age_rating}+ допустим")

    explanation.append(f"совпадение по жанрам: {game.genres}")
    explanation.append(f"рейтинг игры {game.rating}")

    return ", ".join(explanation)