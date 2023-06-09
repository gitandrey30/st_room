import datetime
from typing import List, Callable
from fastapi import APIRouter, Depends, HTTPException, status, Form
from jose import jwt
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response, RedirectResponse, HTMLResponse
from fastapi.requests import Request
from .models import users
from .schemas import User, UserLogin, Token, UserPatch
from database import get_session
from .service import Auth

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

auth = Auth()


@auth_router.get('/users')
async def get_users(session: AsyncSession = Depends(get_session)) -> List[User]:
    query = select(users)
    result = await session.execute(query)
    print(result)
    return result.all()


@auth_router.get("/user/{id}")
async def get_data(id: int, session: AsyncSession = Depends(get_session)) -> User:
    data = select(users).where(users.c.id == id)
    result = await session.execute(data)
    if not id:
        raise HTTPException(status_code=404, detail="id didn't find")
    return result.first()


@auth_router.post('/add_user/')
async def add_user(user_data: User, session: AsyncSession = Depends(get_session)):
    print(user_data)
    query = insert(users).values(**user_data.dict())
    print(query)
    await session.execute(query)
    await session.commit()
    return 'addition complete'


@auth_router.patch('/user/{id}')
async def user_patch(id: int, user_patch: UserPatch, session: AsyncSession = Depends(get_session)) -> UserPatch:
    obj_to_upd = dict(user_patch)
    print(obj_to_upd)
    for data in obj_to_upd.copy():
        if obj_to_upd[data] == None:
            obj_to_upd.pop(data)
    storage = update(users).where(users.c.id == id).values(**obj_to_upd)
    await session.execute(storage)
    await session.commit()
    new_data = select(users).where(users.c.id == id)
    to_tranzaction = await session.execute(new_data)
    return to_tranzaction.first()


@auth_router.delete("/delete_user/{user_id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    data = delete(users).where(users.c.id == id)
    await session.execute(data)
    await session.commit()
    return {'result': 'ok'}


@auth_router.post("/login")
async def get_auth(data: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        user = select(users).where(users.c.email == data.email)
        get_user = await session.execute(user)
        if data.password == get_user.fetchone()[3]:
            print(get_user)
            access_token = auth.encode_access_token(data.email)
            refresh_token = auth.encode_refresh_token(data.email)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            raise HTTPException(status_code=401, detail='email or password is invalid')
    except Exception:
        raise HTTPException(status_code=401, detail='From try: email or password is invalid')


@auth_router.post('/refresh')
async def refresh_token(request: Request, refresh: Token):
    refresh_token = refresh
    return auth.get_new_refresh_or_401(refresh_token.refresh)


@auth_router.get('/get_all_users')
async def get_all_users(request: Request, session: AsyncSession = Depends(get_session)) -> List[User]:
    try:
        access_token = request.headers.get('authorization')
        if auth.decode_access_token(access_token):
            users_query = select(users)
            all_users = await session.execute(users_query)
            return all_users.all()
    except Exception:
        raise HTTPException(status_code=401, detail='auth data not provided')


