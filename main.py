from fastapi import FastAPI
from pydantic import BaseModel
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)
client_db = client["test_mongo"]
collection = client_db["student"]

app = FastAPI()
class Student(BaseModel):
    id: int
    name: str
    age: int

@app.post("/abc/add_student")
async def add_student(student: Student):
    student_dict = student.dict()
    result = await collection.insert_one(student_dict)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/abc/get_students")
async def get_students():    
    students = []
    cursor = collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        students.append(document)
    return students