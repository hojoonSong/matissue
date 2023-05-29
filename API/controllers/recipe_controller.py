from models.recipe import RecipeBase
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def yummy():
    return {"recipe": "😋"}


@router.get("/db")
async def fetch_db():
    return db


@router.post("/db")
async def register_db(recipe: Recipe):
    db.append(recipe)
    return {"recipe_title": recipe.recipe_title, "full": recipe}


@router.delete("/db/{recipe_id}")
async def delete_db(recipe_id: UUID):
    for recipe in db:
        if recipe.recipe_id == recipe_id:
            db.remove(recipe)
            return {"msg": "success"}


@router.patch("/db/{recipe_id}")
async def delete_db(recipe_id: UUID):
    for recipe in db:
        if recipe.recipe_id == recipe_id:
            db.remove(recipe)
            return {"msg": "success"}
