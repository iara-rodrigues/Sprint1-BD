from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models

app = _fastapi.FastAPI()

_services.create_database()



@app.post("/users/", response_model=_schemas.User, status_code=200)
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise _fastapi.HTTPException(
            status_code= 409, detail="Esse nome de usuario ja esta em uso"
        )
    return _services.create_user(db=db, user=user)




@app.get("/users/{user_username}/{user_password}")
def read_user(
    user_username: str, user_password: str, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_username(db=db, username=user_username)
    
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=401, detail= "Não possui uma conta nesse nome de usuário."
        )
        
    else:
        if (user_password == db_user.hashed_password):
            return {"username": user_username,
                    "user_id": db_user.id}
        else:
            raise _fastapi.HTTPException(
                status_code=403, detail= "A senha está errada."
            )
        