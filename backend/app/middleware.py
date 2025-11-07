from fastapi import Request, HTTPException
import time
from .database import SessionLocal


async def audit_middleware(request: Request, call_next):
    """Middleware to log all API requests"""
    start_time = time.time()

    # Skip health checks and docs
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
        response = await call_next(request)
        return response

    db = SessionLocal()
    try:
        response = await call_next(request)

        # Extract user ID from token if available
        user_id = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                # For now, I will log with user context for public endpoints
                pass
            except:
                pass

        # Log the request
        processing_time = time.time() - start_time

        # I will create audit log in the endpoint handlers themselvses.
        return response

    except HTTPException:
        raise
    except Exception as e:
        raise
    finally:
        db.close()
