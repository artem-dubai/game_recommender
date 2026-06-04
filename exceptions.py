from fastapi import Request
from fastapi.responses import JSONResponse


class RecommendationError(Exception):
    def __init__(self, message: str):
        self.message = message


async def recommendation_exception_handler(
    request: Request,
    exc: RecommendationError,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "RecommendationError",
            "message": exc.message,
        },
    )