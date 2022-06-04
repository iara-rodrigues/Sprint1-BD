import sqlalchemy.orm as _orm
import models as _models, schemas as _schemas, database as _database
#from models import User

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()

def get_user_by_username(db: _orm.Session, username: str):
    return db.query(_models.User).filter(_models.User.username == username).first()

def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password 
    db_user = _models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
