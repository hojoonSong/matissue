import pymongo

# MongoDB 연결 설정
client = pymongo.MongoClient(
    'mongodb+srv://shinyubin18:DDYxIIRc0DJKS1Cn@fast.tfq6irt.mongodb.net/')
db = client['FAST']
collection = db['recipes']

# 모든 코멘트의 like 필드를 []로 업데이트
collection.update_many({}, {"$set": {"recipe_like": []}})
