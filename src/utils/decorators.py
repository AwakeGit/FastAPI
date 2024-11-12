import functools
from fastapi.responses import JSONResponse

from src.utils.exceptions import FileTooLargeError, DocumentNotFoundError


def exception_handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileTooLargeError as e:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": str(e)
                }
            )
        except DocumentNotFoundError as e:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": str(e)
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": str(e)
                }
            )

    return wrapper
