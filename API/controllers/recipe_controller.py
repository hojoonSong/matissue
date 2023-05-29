from models.recipe import RecipeBase
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def yummy():
    return {"recipe": "😋"}
