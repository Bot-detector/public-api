from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start time
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # End time
        end_time = time.time()

        # Calculate request processing time
        process_time = end_time - start_time

        log_info = {
            "Request Method": request.method,
            "Request URL": str(request.url),
            "Response Status Code": response.status_code,
            "Processing Time": f"{process_time:.4f}s",
        }
        # Log the request
        logger.info(log_info)

        return response
