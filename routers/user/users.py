from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import routers.user.crud as crud, models, routers.user.schemas as schemas
from database import SessionLocal, engine
from jose import JWTError,jwt


models.Base.metadata.create_all(bind=engine)

SECRET_KEY='505c8ad00a3da230699fd1191368a50acb956314bfb59cc49d6ec1fa898bbccb'
ALGORITHM ='HS256'

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/login")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/login",response_model=schemas.Token)
async def get_token(user:schemas.UserCreate,db:Session=Depends(get_db)):
    user = crud.authenticate_user(user.email,user.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate User")
    token = crud.create_access_token(user.email,user.username,timedelta(minutes=20))
    return JSONResponse({
        'access_token':token,
        'token_type':'bearer'
    })

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/get-current-user")
async def get_current_user(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email : str = payload.get('email')
        username : str = payload.get('username')
        if username is None or email is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
        return JSONResponse({
            'username':username,
            'email':email
        })
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")