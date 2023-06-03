from models.response_models import ErrorResponse

common_responses = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    429: {"model": ErrorResponse, "description": "Too Many Requests"},
}
