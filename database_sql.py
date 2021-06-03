from app import article
from pymongo import MongoClient
import datetime as dt
from data import Articles


connect = MongoClient("mongodb+srv://1234:1234@cluster0.j8pke.mongodb.net/gangnam?retryWrites=true&w=majority")

db = connect.gangnam

col = db.article

article = Articles('ti','de','au','ed')
# article = {
#     'title' : 'html',
#     'description' : '웹 페이지 확장자',
#     'author' : 'jeong',
#     'array' : [1,2,3,4,5,6,7,8,9,10],
#     'age':10,
#     'create_at' : dt.datetime.now()
# }

# 데이터 입력
col.insert(article)

# 데이터 전체 출력
data = col.find()
for i in data:
    print(i)

# 데이터 검색
# data = col.find_one({"title":"flask"})
# for i in data:
#     print(i)
# print(data)

# result = col.find({"나이": {"$gt" : 40, "$lte": 50}},{"_id":False, "나이":True})
# for r in result:
#     print(r)

# data = col.find({"age":{"$gt":5,"&lte":11}})
# for r in data:
#     print(r)