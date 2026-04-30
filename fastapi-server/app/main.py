from fastapi import FastAPI, Depends, HTTPException
import status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
import calculator_module as cm
import uvicorn
import models.user as s_u
from database.database import get_db_connection
import asyncpg
from security.security import hash_password, verify_password, create_jwt_token, get_user_from_token

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: asyncpg.Connection = Depends(get_db_connection)):
    result = await db.fetchrow('''
        SELECT email, name, hash_password FROM users WHERE email = $1
    ''', form_data.username)

    if not result or not verify_password(form_data.password, result["hash_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": result["email"], "name": result["name"]}
    access_token = create_jwt_token(token_data)

    return access_token

@app.get('/protected')
async def protected_route(current_user: str = Depends(get_user_from_token)):
    return {"message": f"Hello {current_user}, you are authenticated!"}

@app.get('/eval')
async def solving_expression(expression: str = ""):
    if (len(expression) == 0):
        return {"result": 0}
    else:
        return {"result": cm.eval(expression)}

@app.post('/create_user')
async def create_user(new_user: s_u.PostUser, db: asyncpg.Connection = Depends(get_db_connection)):
    hashed_password = hash_password(new_user.password)
    try:
        await db.execute('''
            INSERT INTO users (email, name, hash_password) VALUES($1, $2, $3)
        ''', new_user.email, new_user.name, hashed_password)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    return {"message": f"{new_user.name} added successfully"}

@app.delete('/delete_user')
async def delete_user(user: s_u.DeleteUser, db: asyncpg.Connection = Depends(get_db_connection), current: str = Depends(get_user_from_token)):
    if current != user.email:
        raise HTTPException(status_code=403, detail="Can only delete your own account")
    
    result = await db.fetchrow('''
        SELECT hash_password FROM users WHERE users.email = $1
    ''', user.email)
    
    if not result or not verify_password(user.password, result['hash_password']):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    delete_result = await db.execute('''
        DELETE FROM users WHERE users.email = $1
    ''', user.email)
    
    if delete_result == "DELETE 0":
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

@app.patch('/change_name')
async def change_name(new_name_user: s_u.PatchUser, db: asyncpg.Connection = Depends(get_db_connection), current: str = Depends(get_user_from_token)):
    if current != new_name_user.email:
        raise HTTPException(status_code=403, detail="Can only change your own name")
    
    result = await db.fetchrow('''
        SELECT hash_password FROM users WHERE users.email = $1
    ''', new_name_user.email)
    
    if not result or not verify_password(new_name_user.hash_password, result['hash_password']):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    patch_result = await db.execute('''
        UPDATE users
        SET name = $1
        WHERE email = $2
    ''', new_name_user.name, new_name_user.email)

    if patch_result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Username changed succesfully"}


if __name__ == "__main__":
    uvicorn.run(app)

