from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from typing import List
from uuid import UUID, uuid4
from bson import ObjectId


class Category(str, Enum):
    korean = "korean"
    chinese = "chinese"
    japanese = "japanese"
    western = "western"
    vegetarian = "vegetarian"
    other = "other"


class Ingredients(BaseModel):
    name: str
    amount: str


class Information(BaseModel):
    serving: int  # 인원
    time: int  # 조리시간
    level: int  # 난이도


class SequenceItem(BaseModel):
    picture: str  # url 들어갈예정
    description: str


class Recipe(BaseModel):
    recipe_id: str = Field(default=0)
    recipe_title: str
    recipe_thumbnail: str
    recipe_video: str
    recipe_description: str
    recipe_category: List[Category]
    recipe_info: str
    recipe_ingredients: List[Ingredients]
    recipe_sequence: List[SequenceItem]
    recipe_tip: str
    recipe_like: int = Field(default=0)
    user_id: str
