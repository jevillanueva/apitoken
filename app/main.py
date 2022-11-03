from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app.auth.access import get_actual_user
from app.core import configuration
from app.routers import oauth_google, users, token

TITLE = configuration.APP_TITLE
VERSION = configuration.APP_VERSION
app = FastAPI(
    title=TITLE,
    version=VERSION,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    SessionMiddleware, secret_key=configuration.APP_SECRET_KEY_MIDDLEWARE
)


@app.get("/", tags=["Index"])
def read_root():
    return {"title": TITLE, "version": VERSION}


@app.get("/api/docs", tags=["Documentation"])  # Tag it as "documentation" for our docs
async def get_documentation(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = get_swagger_ui_html(
        openapi_url="/api/openapi.json", title="Documentation"
    )
    return response


@app.get("/api/openapi.json", tags=["Documentation"])
async def get_open_api_endpoint(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = JSONResponse(
        get_openapi(title=TITLE, version=VERSION, routes=app.routes)
    )
    return response


@app.get("/api/redoc", tags=["Documentation"])  # Tag it as "documentation" for our docs
async def redoc_html(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = get_redoc_html(openapi_url="/api/openapi.json", title="Documentation")
    return response


app.include_router(oauth_google.router, prefix="/api/google", tags=["Security Google"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(token.router, prefix="/api/token", tags=["Token"])