from fastapi import APIRouter, Depends
from app.models import User, User_Pydantic, UserIn_Pydantic
from passlib.hash import bcrypt
from app.auth import get_current_user

router = APIRouter(
    tags=['User']
)

@router.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic): # type: ignore
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)): # type: ignore
    return user    
