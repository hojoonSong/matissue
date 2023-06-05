from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, Field, Extra
from typing import List
from nanoid import generate


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


class LevelEnum(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class Information(BaseModel):
    serving: int  # 인원
    time: int  # 조리시간
    level: LevelEnum  # 난이도


class SequenceItem(BaseModel):
    step: int  # url 들어갈예정
    picture: str  # url 들어갈예정
    description: str


class RecipeBase(BaseModel):
    recipe_title: str
    recipe_thumbnail: str
    recipe_video: str
    recipe_description: str
    recipe_category: Category
    recipe_info: Information
    recipe_ingredients: List[Ingredients]
    recipe_sequence: List[SequenceItem]
    recipe_tip: str


class RecipeCreate(RecipeBase):
    recipe_id: str = Field(default_factory=lambda: generate(), exclude=True)
    recipe_view: int = Field(default=0, exclude=True)
    user_id: str
    user_nickname: str = Field(default='test', exclude=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, exclude=True)
    recipe_like: int = Field(default=0, exclude=True)


class RecipeGetOne(BaseModel):
    recipe_title: str
    recipe_thumbnail: str
    recipe_id: str
    recipe_view: int
    user_id: str
    user_nickname: str
    created_at: datetime
    recipe_like: int


class RecipeGetMany(BaseModel):
    recipes: List[RecipeGetOne]


class RecipeView(RecipeBase):
    recipe_view: int


class RecipeLike(RecipeBase):
    recipe_like: int

# class RecipeList(RecipeBase):
#     recipe_id: str = Field(default_factory=lambda: generate())
#     recipe_title: str
#     recipe_thumbnail: str
#     recipe_like: int = Field(default=0)
#     user_id: str


# class RecipeSearchByCategory(RecipeBase):
# class RecipeSearchByTime(RecipeBase):
# class RecipeSearchByIngredient(RecipeBase):
