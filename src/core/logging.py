import time
import logging
from fastapi import Request, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f'{process_time:.2f}ms'

    logger.info(f"Request: {request.method} {request.url.path} - Completed in {formatted_process_time} - Status Code: {response.status_code}")
    
    return response
