from bson.objectid import ObjectId
from fastapi import HTTPException, status, Body, Depends, APIRouter
from pymongo import MongoClient

from apps.auth.auth_bearer import JWTBearer, get_jwt_subject
from apps.auth.auth_handler import sign_jwt
from apps.categories.models import Category
from db import db

router = APIRouter()
cat_collection = db['categories']


@router.get("/")
async def get_categories():
    categories = []
    for cat in cat_collection.find():
        cat["_id"] = str(cat["_id"])
        categories.append(cat)
    return categories

@router.post("/")
async def create_category(cat: Category = Body(default=None)):
    cat_dict = cat.dict()
    result = cat_collection.insert_one(cat_dict)
    cat_dict["_id"] = str(result.inserted_id)
    return cat_dict
