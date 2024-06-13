import datetime
import firebase_admin
from firebase_admin import auth  # Added import
from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN
import secrets

account_key_path = "app/service-account-file.json"
cred = firebase_admin.credentials.Certificate(account_key_path)
firebase_admin.initialize_app(cred)

async def firebase_auth_middleware(request: Request, call_next):

    allow_list_endpoints = ["/docs", "/openapi.json", "/"]

    if request.url.path in allow_list_endpoints:
        response = await call_next(request)
        return response

    # Get the token from the request headers
    token = request.headers.get("Authorization", None).split(" ")[-1]
    if not token:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    try:
        # Verify the token
        r = auth.verify_id_token(token)
        print("the response", r)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )
    except auth.InvalidIdTokenError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid ID token",
        )
    except auth.ExpiredIdTokenError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Expired ID token",
        )
    except auth.RevokedIdTokenError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Revoked ID token",
        )
    except auth.UserDisabledError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User is disabled",
        )

    # If the token is valid, let the request pass
    response = await call_next(request)
    return response