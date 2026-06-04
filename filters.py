def filter_games(user, recommendations):
    filtered = []

    for game, score in recommendations:

        if game.platform != user.preferred_platform:
            continue

        if game.price > user.max_price:
            continue

        if game.playtime > user.max_playtime:
            continue

        if game.age_rating > user.max_age_rating:
            continue

        if game.region != user.region:
            continue

        filtered.append((game, score))

    return filtered[:10]