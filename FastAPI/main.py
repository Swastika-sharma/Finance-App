from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
tags_metadata = [
    {
        "name": "FinanceAPI",
    }
]
origins = [
    'http://localhost:3000',
]
#to store the data in db
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        form_attributes = True #orm_mode updated


#Dependency to get the session to db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)
@app.get("/", tags=['Root'])
async def root():
    return {"message": "Hello World"}

@app.post("/transactions/", tags=['FinanceAPI'], response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", tags=['FinanceAPI'], response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int=0, limit: int=100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions
    