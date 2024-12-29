import templates
from fastapi import FastAPI, status, Body, HTTPException, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

class User(BaseModel):
    id: int
    age: int
    username: str

@app.get('/')
async def get_(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "user": users[user_id-1]})

@app.post('/user/{username}/{age}')
async def user_register(username: Annotated[str, Path(ge=5, le=20,
                                             description="Enter username",
                                             examples="UrbanUser")],
                        age: Annotated[int, Path(ge=18, le=120,
                                       description="Enter age",
                                       examples="24")]) -> dict:
    len_user = len(username)
    if len_user == 0:
        username.id = 1
    else:
        username.id = users[len_user - 1].id + 1
    username.username = username
    username.age = age
    username.append(users)
    return f'User {username} is registered'

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path (ge=1, le=100,
                                           description='Enter User ID',
                                           examples="1")],
                      username: Annotated[str, Path(ge=5, le=20,
                                             description="Enter username",
                                             examples="UrbanUser")],
                      age:Annotated[int, Path(ge=18, le=120,
                                       description="Enter age",
                                       examples="24")]) -> str:
    try:
        update_user = users[user_id - 1]
        update_user.username = username
        update_user.age = age
        return update_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path (ge=1, le=100,
                                           description='Enter User ID',
                                           examples="1")]) -> str:
    for i, u in enumerate(users):
        if u.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail='User was not found')