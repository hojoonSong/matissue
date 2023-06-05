from enum import IntEnum
from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, Field, Extra
from typing import List, Optional
from nanoid import generate


class Category(str, Enum):
    korean = "korean"
    chinese = "chinese"
    japanese = "japanese"
    western = "western"
    vegetarian = "vegetarian"
    other = "other"

    class Config:
        schema_extra = {
            "example": {
                "recipe_category": "korean"
            }
        }


class Ingredients(BaseModel):
    name: str
    amount: str

    class Config:
        schema_extra = {
            "example": {
                "name": "오이",
                "amount": "1개"
            }
        }


class LevelEnum(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class Information(BaseModel):
    serving: int  # 인원
    time: int  # 조리시간
    level: LevelEnum  # 난이도

    class Config:
        schema_extra = {
            "example": {
                "serving": 0,
                "time": 10,
                "level": 0
            }
        }


class SequenceItem(BaseModel):
    step: int  # url 들어갈예정
    picture: str  # url 들어갈예정
    description: str

    class Config:
        schema_extra = {
            "example": {
                "step": 1,
                "picture": "url",
                "description": "순두부를 자른다."
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "recipe_title": "삼겹덮밥",
                "recipe_thumbnail": "url",
                "recipe_video": "url",
                "recipe_description": "삼겹살을 덮은 덮밥",
                "recipe_category": 'korean',
                "recipe_info": {'serving': 0, 'time': 10, 'level': 0},
                "recipe_ingredients": [{'name': '오이', 'amount': '1개'}],
                "recipe_sequence": [
                    {
                        "step": 1,
                        "picture": "url",
                        "description": "밥을 짓는다."
                    },
                    {
                        "step": 2,
                        "picture": "url",
                        "description": "삼겹살을 굽는다."
                    },
                    {
                        "step": 3,
                        "picture": "url",
                        "description": "밥위에 덮는다."
                    }
                ],
                "recipe_tip": "맛있다",
            }
        }


class RecipeCreate(RecipeBase):
    recipe_id: str = Field(default_factory=lambda: generate())
    recipe_view: int = Field(default=0)
    user_id: str
    user_nickname: str = Field(default='test')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    recipe_like: int = Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "recipe_title": "삼겹덮밥",
                "recipe_thumbnail": "url",
                "recipe_video": "url",
                "recipe_description": "삼겹살을 덮은 덮밥",
                "recipe_category": 'korean',
                "recipe_info": {'serving': 0, 'time': 10, 'level': 0},
                "recipe_ingredients": [{'name': '오이', 'amount': '1개'}],
                "recipe_sequence": [
                    {
                        "step": 1,
                        "picture": "url",
                        "description": "밥을 짓는다."
                    },
                    {
                        "step": 2,
                        "picture": "url",
                        "description": "삼겹살을 굽는다."
                    },
                    {
                        "step": 3,
                        "picture": "url",
                        "description": "밥위에 덮는다."
                    }
                ],
                "recipe_tip": "맛있다",
                "user_id": "test",
                "user_nickname": "test",
                "created_at": "자동생성",
                "recipe_id": "자동생성",
                "recipe_view": "자동생성",
                "recipe_like": "자동생성"
            }
        }


class RecipeUpdate(BaseModel):
    recipe_title: Optional[str]
    recipe_thumbnail: Optional[str]
    recipe_video: Optional[str]
    recipe_description: Optional[str]
    recipe_category: Category
    recipe_info: Information
    recipe_ingredients: List[Ingredients]
    recipe_sequence: List[SequenceItem]
    recipe_tip: Optional[str]
    # user_nickname: Optional[str] = Field(default='test')
    # recipe_id: Optional[str] = Field(default_factory=lambda: generate())
    # recipe_view: Optional[str] = Field(default=0)
    # user_id: str
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # recipe_like: Optional[str] = Field(default=0)


class RecipeGetItem(BaseModel):
    recipe_title: str
    recipe_thumbnail: str
    recipe_id: str
    recipe_view: int
    user_id: str
    user_nickname: str
    created_at: datetime
    recipe_like: int

    class Config:
        schema_extra = {
            "example": {
                "recipe_title": "삼겹덮밥",
                "recipe_thumbnail": "0",
                "recipe_id": "QRCqp6ZFAZWt9NcMO6q1B",
                "recipe_view": "0",
                "user_id": "test",
                "user_nickname": "test",
                "created_at": "2023-06-05 08:15:13.806000",
                "recipe_like": "0"
            }
        }


class RecipeGetList(BaseModel):
    recipes: List[RecipeGetItem]


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
