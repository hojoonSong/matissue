from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.user_models import UserInDB
from fastapi import HTTPException
from typing import List
import asyncio

settings = get_settings()


class UserDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("users")

    async def create_user_in_db(self, user_in_db: UserInDB):
        # subscriptions와 fans를 set에서 list로 변환
        if isinstance(user_in_db.subscriptions, set):
            user_in_db.subscriptions = list(user_in_db.subscriptions)
        if isinstance(user_in_db.fans, set):
            user_in_db.fans = list(user_in_db.fans)

        # 데이터베이스에 삽입
        result = await self.collection.insert_one(user_in_db.dict())
        return str(result.inserted_id)

    async def update_user_in_db(self, user_id: str, update_data: dict):
        result = await self.collection.update_one(
            {"user_id": user_id}, {"$set": update_data}
        )
        return result.modified_count == 1

    async def delete_user(self, user_id: str):
        delete_result = await self.collection.delete_one({"user_id": user_id})
        return delete_result.deleted_count > 0

    async def get_user_by_id(self, user_id: str):
        user_doc = await self.collection.find_one({"user_id": user_id})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_user_by_email(self, email: str):
        user_doc = await self.collection.find_one({"email": email})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_username_by_id(self, user_id: str):
        user = await self.get_user_by_id(user_id)
        if user:
            return user.username
        return None

    async def get_user_by_email_and_birthdate(self, email: str, birthdate: str):
        user_doc = await self.collection.find_one(
            {"email": email, "birthdate": birthdate}
        )
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_user_by_id_and_birthdate(self, user_id: str, birthdate: str):
        user_doc = await self.collection.find_one(
            {"user_id": user_id, "birthdate": birthdate}
        )
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_users(self):
        user_docs = self.collection.find({})
        users = []
        async for user_doc in user_docs:
            users.append(UserInDB(**user_doc))
        return users

    async def get_user_by_email_and_birthdate(self, email: str, birthdate: str):
        user_doc = await self.collection.find_one(
            {"email": email, "birth_date": birthdate}
        )
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_user_by_id_and_birthdate(self, user_id: str, birthdate: str):
        user_doc = await self.collection.find_one(
            {"user_id": user_id, "birth_date": birthdate}
        )
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def modify_subscription(
        self, current_user: str, follow_user_id: str, subscribe: bool
    ) -> None:
        # 데이터를 동시에 불러옵니다.
        user, follow_user = await asyncio.gather(
            self.get_user_by_id(current_user),
            self.get_user_by_id(follow_user_id),
        )

        if not user or not follow_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        # 구독 체크
        if current_user == follow_user_id:
            raise HTTPException(status_code=400, detail="본인을 구독 할 수 없습니다.")

        # None 처리
        user.subscriptions = user.subscriptions or set()
        follow_user.fans = follow_user.fans or set()

        if subscribe:
            user.subscriptions.add(follow_user_id)
            follow_user.fans.add(current_user)
        else:
            user.subscriptions.discard(follow_user_id)
            follow_user.fans.discard(current_user)

        # 데이터베이스를 동시에 업데이트 합니다 (set을 list로 변환).
        await asyncio.gather(
            self.update_user_in_db(
                current_user, {"subscriptions": list(user.subscriptions)}
            ),
            self.update_user_in_db(follow_user_id, {"fans": list(follow_user.fans)}),
        )

    async def get_user_details(self, user_ids: List[str]):
        cursor = self.collection.find({"user_id": {"$in": user_ids}})
        people = []
        async for doc in cursor:
            person = UserInDB(**doc)
            people.append(
                {
                    "user_id": person.user_id,
                    "username": person.username,
                    "img": person.img,
                }
            )
        return people

    async def get_fans(self, user_id: str):
        doc = await self.collection.find_one({"user_id": user_id})
        if doc and "fans" in doc:
            return await self.get_user_details(doc["fans"])
        return []

    async def get_subscriptions(self, user_id: str):
        doc = await self.collection.find_one({"user_id": user_id})
        if doc and "subscriptions" in doc:
            return await self.get_user_details(doc["subscriptions"])
        return []

    async def is_user_subscribed(self, current_user: str, follow_user_id: str) -> bool:
        user_doc = await self.collection.find_one(
            {"user_id": current_user, "subscriptions": follow_user_id},
            projection={"subscriptions": 1},
        )

        return user_doc is not None


def get_user_dao() -> UserDao:
    db_manager = MongoDBManager()
    return UserDao(db_manager)
