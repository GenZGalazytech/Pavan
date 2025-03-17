from fastapi import APIRouter
from Controllers.controllers import register,login,get_all_users, search_images
from models.models import Message, User,Userlogin



router = APIRouter()

@router.get('/test')
async def test():
    return {"hello"}

@router.post('/register')
async def register_user(user : User):
    return register(user)

@router.post('/login')
async def login_user(user: Userlogin):
    return login(user)

@router.get('/all')
async def get_users():
    return get_all_users()

@router.post('/chat')
def chat_bot(message:Message):
    return search_images(message)
