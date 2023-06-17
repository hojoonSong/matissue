from enum import IntEnum
from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, Field, Extra
from typing import List, Optional
from nanoid import generate
from dataclasses import dataclass
from pydantic import BaseModel


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
    picture: str
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


class RecipeIn(BaseModel):
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
    user_id: Optional[str]
    user_nickname: Optional[str] = Field(default='test')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    recipe_like: Optional[List[str]] = []

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
                "recipe_tip": "맛있다"
            }
        }


class RecipeUpdate(BaseModel):
    recipe_title: Optional[str]
    recipe_thumbnail: Optional[str]
    recipe_video: Optional[str]
    recipe_description: Optional[str]
    recipe_category: Optional[Category]
    recipe_info: Optional[Information]
    recipe_ingredients: Optional[List[Ingredients]]
    recipe_sequence: Optional[List[SequenceItem]]
    recipe_tip: Optional[str]
    user_nickname: Optional[str]

    class Config:
        schema_extra = {
            "example":    {
                "recipe_title": "수정테스트",
                "recipe_thumbnail": "https://eliceproject.s3.ap-northeast-2.amazonaws.com/20230602073742667_dino.png",
                "recipe_video": "youtube.com/watch?v=AdMgVkp4OXI",
                "recipe_description": "수정테스트",
                "recipe_category": "korean",
                "recipe_info": {
                    "serving": 3,
                    "time": 60,
                    "level": 1
                },
                "recipe_ingredients": [
                    {
                        "name": "수정테스트",
                        "amount": "수정테스트"
                    },
                    {
                        "name": "소금",
                        "amount": "적당량"
                    }
                ],
                "recipe_sequence": [
                    {
                        "step": 1,
                        "picture": "https://eliceproject.s3.ap-northeast-2.amazonaws.com/20230602073742667_dino.png",
                        "description": "수정테스트)설명"
                    },
                    {
                        "step": 2,
                        "picture": "https://eliceproject.s3.ap-northeast-2.amazonaws.com/20230602073742667_dino.png",
                        "description": "수정테스트)설명"
                    },
                    {
                        "step": 3,
                        "picture": "https://eliceproject.s3.ap-northeast-2.amazonaws.com/20230602073742667_dino.png",
                        "description": "수정테스트)설명"
                    }
                ],
                "recipe_tip": "수정테스트)팁",
            }
        }


class RecipeGetItem(BaseModel):
    recipe_title: str
    recipe_thumbnail: str
    recipe_id: str
    recipe_view: int
    user_id: str
    user_nickname: str
    created_at: datetime
    recipe_like: Optional[List[str]] = []

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
    recipe_like: Optional[List[str]] = []


class CommentBase(BaseModel):
    comment_author: str
    comment_nickname: str
    comment_profile_img: str
    comment_text: str
    comment_like: Optional[List[str]] = []
    comment_id: str = Field(default_factory=lambda: generate())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    comment_parent: str


class CommentUpdate(BaseModel):
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    comment_nickname: Optional[str]
    comment_profile_img: Optional[str]
    comment_text: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "comment_text": "수정테스트",
            }
        }


class CommentIn(BaseModel):
    comment_text: str

    class Config:
        schema_extra = {
            "example": {
                "comment_text": "와 정말 맛있겠어요"
            }
        }


class CommentsList(BaseModel):
    recipes: List[CommentBase]


class CommentLike(BaseModel):
    comment_like: Optional[List[str]] = []
