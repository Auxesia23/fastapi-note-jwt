from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from routers import token, user, note
from config import TORTOISE_ORM

app = FastAPI()
app.include_router(token.router)
app.include_router(user.router)
app.include_router(note.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


register_tortoise(
    app, 
    config=TORTOISE_ORM,
    add_exception_handlers=True
)
