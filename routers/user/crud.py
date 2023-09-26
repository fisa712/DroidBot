from datetime import datetime
from sqlalchemy.orm import Session
import models, routers.user.schemas as schemas
from jose import jwt
from passlib.context import CryptContext



SECRET_KEY='505c8ad00a3da230699fd1191368a50acb956314bfb59cc49d6ec1fa898bbccb'
ALGORITHM ='HS256'

crypto_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    hashed_password =crypto_context.hash(user.password)
    db_user = models.User(email=user.email,username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(email,password,db:Session):
    user =  db.query(models.User).filter(models.User.email==email).first()
    if not user:
        return False
    if not crypto_context.verify(password,user.password):
        return False
    return user


def create_access_token(email,username,expires_time):
    encode={'email':email,'username':username}
    # expires = datetime.now()  + expires_time
    # encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


