from fastapi import APIRouter, Path, HTTPException
from typing import List
from starlette.responses import JSONResponse
from starlette.status import *
from .model_user import UserSchema, UserDB
from db import database, tbl_users
from starlette.status import *

# import user model and services
from .model_user import UserSchema, UserDB, UserResponseSchema

async def dBcreateUser(user: UserSchema):
    try:
        query = tbl_users.insert().values(
            user_name=user.userName,
            first_name=user.firstName,
            last_name=user.lastName
        )
        return await database.execute(query=query)
    except Exception as e:
        return {
            'status_code': HTTP_400_BAD_REQUEST,
            'description': e.detail
        }

async def dBgetAllUsers():
    query = tbl_users.select()
    return await database.fetch_all(query=query)


async def dBgetUser(id: int):
    query = tbl_users.select().where(id == tbl_users.c.id)
    return await database.fetch_one(query=query)


async def dBupdateUser(id: int, user: UserSchema):
    query = (
        tbl_users
        .update()
        .where(id == tbl_users.c.id)
        .values(first_name=user.firstName, last_name=user.lastName)
        .returning(tbl_users.c.id, tbl_users.c.first_name, tbl_users.c.last_name, tbl_users.c.user_name)
    )
    return await database.fetch_one(query=query)


async def dBdeleteUser(id: int):
    query = tbl_users.delete().where(id == tbl_users.c.id)
    return await database.execute(query=query)

# ===========================================================


router = APIRouter()

# POST
# Creates a new User
@router.post("/createUser")
async def createUser(user: UserSchema):
    user_primary_key = await dBcreateUser(user)
    if isinstance(user_primary_key, dict):
        print(user_primary_key)
        raise HTTPException(
            status_code=user_primary_key['status_code'], detail=user_primary_key['description'])
    user_response = {
        "id": user_primary_key,
        "userName": user.userName,
        "firstName": user.firstName,
        "lastName": user.lastName
    }
    return JSONResponse(status_code=HTTP_201_CREATED, content=user_response)


# GET
# RETURNS ALL DATA AS A LIST OF DICTIONARIES(JSON)
@router.get("/getAllUsers", response_model=List[UserResponseSchema])
async def getAllUsers():
    return await dBgetAllUsers()

# GET ALL USERS
# RETURNS ALL DETAILS
@router.get("/{id}/", response_model=UserResponseSchema)
async def getUser(id: int = Path(..., gt=0),):
    user = await dBgetUser(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/updateUser/{id}/", response_model=UserResponseSchema)
async def updateUser(user: UserSchema, id: int = Path(..., gt=0),):
    userExist = await dBgetUser(id)
    if not userExist:
        raise HTTPException(status_code=404, detail="User not found")

    updatedUser = await dBupdateUser(id, user)
    return updatedUser


@router.delete("/deleteUser/{id}/", response_model=UserResponseSchema)
async def deleteUser(id: int = Path(..., gt=0)):
    userExist = await dBgetUser(id)
    if not userExist:
        raise HTTPException(status_code=404, detail="User not found")

    await dBdeleteUser(id)
    return userExist
