from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.user_models import UserInDB
from fastapi import HTTPException

settings = get_settings()


class UserDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("users")

    async def create_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.insert_one(user_in_db.dict())
        return str(result.inserted_id)

    async def update_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.replace_one(
            {"user_id": user_in_db.user_id}, user_in_db.dict()
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
        # async with self.db.transaction():  # Database Transaction
        user = await self.get_user_by_id(current_user)
        follow_user = await self.get_user_by_id(follow_user_id)

        if not user or not follow_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        # 구독 체크
        if current_user == follow_user_id:
            raise HTTPException(status_code=400, detail="본인을 구독 할 수 없습니다.")

        if isinstance(user.subscriptions, list) and isinstance(
            follow_user.fans, list
        ):  # 데이터 타입 체크
            if subscribe:
                if follow_user_id in user.subscriptions:
                    raise HTTPException(status_code=409, detail="이미 구독 중입니다")
                else:
                    user.subscriptions.append(follow_user_id)
                    follow_user.fans.append(current_user)
            else:
                if follow_user_id in user.subscriptions:
                    user.subscriptions.remove(follow_user_id)
                    follow_user.fans.remove(current_user)

                else:
                    raise HTTPException(status_code=409, detail="구독을 취소할 수 없습니다.")
        else:
            raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")

        await self.update_user_in_db(user)
        await self.update_user_in_db(follow_user)

    async def get_people(self, user_id: str, field: str):
        query = {field: user_id}
        docs = self.collection.find(query)
        people = []
        async for doc in docs:
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
        return await self.get_people(str(user_id), "subscriptions")

    async def get_subscriptions(self, user_id: str):
        return await self.get_people(str(user_id), "fans")

    async def is_user_subscribed(self, current_user: str, follow_user_id: str) -> bool:
        user = await self.get_user_by_id(current_user)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return follow_user_id in user.subscriptions


def get_user_dao() -> UserDao:
    db_manager = MongoDBManager()
    return UserDao(db_manager)
