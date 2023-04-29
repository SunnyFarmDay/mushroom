from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}

class Person(BaseModel):
    SID: int
    name: str
    salary: int

DB: List[Person] = [
    Person(1, "POON, Yiu Yeung", 2300)
]

@app.get("")
