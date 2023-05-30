from enum import Enum, IntEnum
from pydantic import BaseModel, Field
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
    time: str  # 조리시간/ FE 담당자와 논의 후 str으로 변경한 상태 코치님과 논의해보면 좋을듯
    level: LevelEnum  # 난이도


class SequenceItem(BaseModel):
    picture: str  # url 들어갈예정
    description: str


class Recipe(BaseModel):
    recipe_id: str = Field(default_factory=lambda: generate())
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
