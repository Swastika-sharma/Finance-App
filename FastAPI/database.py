from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:2001@localhost:5432/finance'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#Dependency to get the session to db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    
        

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='2001', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Is Connected Successfully!")
        break
    except Exception as error:
        print("Connecting To Database Failed")
        print("Error:", error)   
        time.sleep(2) 
        