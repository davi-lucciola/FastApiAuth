from fastapi import FastAPI, Depends
from auth import UserCredentials, create_token, authenticate_user


app = FastAPI()


# Endpoint protegido por autênticação.
@app.get('/me')
async def me(user: dict = Depends(authenticate_user)):
    return user

# Endpoint para realizar o login.
@app.post('/login')
async def login(credentials: UserCredentials):
    token = create_token(credentials.username, credentials.password)
    return {
        'access-token': token,
        'type': 'Bearer'
    }
