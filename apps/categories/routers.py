from bson.objectid import ObjectId
from fastapi import HTTPException, status, Body, Depends, APIRouter

from apps.auth.auth_bearer import JWTBearer, get_current_admin_user
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


@router.get("/{cat_id}")
async def get_category(cat_id: str):
    cat = cat_collection.find_one({"_id": ObjectId(cat_id)})
    if cat:
        cat["_id"] = str(cat["_id"])
        return cat
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.post("/", dependencies=[Depends(JWTBearer()), Depends(get_current_admin_user)])
async def create_category(cat: Category = Body(default=None)):
    cat_dict = cat.dict()
    result = cat_collection.insert_one(cat_dict)
    cat_dict["_id"] = str(result.inserted_id)
    return cat_dict


@router.put("/{cat_id}/edit_data", dependencies=[Depends(JWTBearer()), Depends(get_current_admin_user)])
async def update_category_data(cat_id: str, cat: Category):
    cat_dict = cat.dict(exclude_unset=True)
    result = cat_collection.update_one({"_id": ObjectId(cat_id)}, {"$set": cat_dict})
    if result.modified_count == 1:
        cat_dict["_id"] = cat_id
        return cat_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.delete("/{cat_id}", dependencies=[Depends(JWTBearer()), Depends(get_current_admin_user)])
async def delete_category(cat_id: str):
    result = cat_collection.delete_one({"_id": ObjectId(cat_id)})
    if result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
