from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import time


SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#This one is just for raw sql not for sqlalchemy which we are actually using
# while True:
#     try: 
#         conn=psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password='motherchod2821',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection successfull")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ",error)
#         time.sleep(2)