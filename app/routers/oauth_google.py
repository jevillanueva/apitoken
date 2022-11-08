from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from starlette.requests import Request

from app.core import configuration
from app.models.result import Result
from app.models.user import UserInDB
from app.services.user import UserService
from app.utils import validate_forwarded_proto

router = APIRouter()

oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=configuration.APP_GOOGLE_CLIENT_ID,
    client_secret=configuration.APP_GOOGLE_CLIENT_SECRET,
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_server_side")
    redirect_uri =  validate_forwarded_proto.validateHTTPS(url=redirect_uri, schema=request.headers.get("x-forwarded-proto"))
    google = oauth.create_client('google')
    print(redirect_uri)
    print (request.headers)
    return await google.authorize_redirect(request, redirect_uri)


@router.get("/auth", response_model=Result)
async def auth_server_side(request: Request):
    google = oauth.create_client('google')
    token = await google.authorize_access_token(request)
    print(token)
    user = token.get('userinfo')
    request.session['user'] = dict(user)
    userDB = UserInDB(
        username=user.get("email"),
        email=user.get("email"),
        picture=user.get("picture"),
        given_name=user.get("given_name"),
        family_name=user.get("family_name"),
        disabled=False,
    )
    ret = UserService.insert_or_update_user(userDB)
    return Result(message="Login Success")


@router.get('/logout', response_model=Result)  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    return Result(message="Logout Success")