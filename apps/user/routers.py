from bson.objectid import ObjectId
from fastapi import HTTPException, status, Body, Depends, APIRouter

from apps.auth.auth_bearer import JWTBearer, get_jwt_subject
from apps.auth.auth_handler import sign_jwt
from apps.user.models import UserSchema, UserLoginSchema, UserUpdateSchema
from db import db

router = APIRouter()
users_collection = db['users']


@router.post("/signup")
async def create_user(user: UserSchema = Body(default=None)):
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return sign_jwt(user.email)


@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)):
    result = users_collection.find_one({"email": user.email, "password": user.password})
    if result:
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }


@router.get("/")
async def get_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/{user_id}", dependencies=[Depends(JWTBearer())])
async def update_user(user_id: str, user: UserUpdateSchema, current_user: dict = Depends(get_jwt_subject)):
    if user_id != str(current_user.get("_id")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can only update your own user data")
    user_dict = user.dict(exclude_unset=True)
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    if result.modified_count == 1:
        user_dict["_id"] = user_id
        return user_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/{user_id}", dependencies=[Depends(JWTBearer())])
async def delete_user(user_id: str, current_user: dict = Depends(get_jwt_subject)):
    if user_id != str(current_user.get("_id")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can only delete your own profile")
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
