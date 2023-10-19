from fastapi import FastAPI, Request, HTTPException, Form,APIRouter,Depends
from itsdangerous import URLSafeTimedSerializer
serializer = URLSafeTimedSerializer('as4f')

def generate_session_token(user):
    try:
        token =serializer.dumps({"email": user.email})
        print(f"Generated Token: {token}")
        return token
    except Exception as e:
        print(f"Error generating token: {e}")

def get_user_from_session_token(session_token):
    try:
        user = serializer.loads(session_token)
        return user
    except Exception as e:
        print(f"Error decoding session token: {e}")
        return None

def get_session_token(request: Request):
    return request.cookies.get("session_token")

def get_current_user(token):
    user = get_user_from_session_token(token)
    if user is None :
        raise HTTPException(status_code=302, detail="Not authenticated", headers={"Location": "/login?error=Not+authenticated"})
    return user