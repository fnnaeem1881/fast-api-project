from fastapi import FastAPI, Request, HTTPException, Form,APIRouter,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from db_config import database, connect_to_database, close_database_connection
from Routes.token_key import generate_session_token, get_user_from_session_token,get_session_token,get_current_user
from fastapi.staticfiles import StaticFiles



admin = APIRouter()

templates = Jinja2Templates(directory="templates")

@admin.on_event("startup")
async def startup_db():
    await connect_to_database()

@admin.on_event("shutdown")
async def shutdown_db():
    await close_database_connection()
    

async def get_user_by_email(email):
    user = await database.fetch_one("SELECT * FROM users WHERE email = :email", values={"email": email})
    return user

@admin.route("/dashboard", methods=["GET", "POST"])
async def dashboard(request: Request):
    token = request.cookies.get("session_token")
    user = get_current_user(token)
    print(f"User data: {user}")
    if user:
        email = user['email']
        user_data = await  get_user_by_email(email)
        if user_data and user_data.role == 'admin':
            return templates.TemplateResponse("admin/index.html", {"request": request, "user": user_data})
        elif  user_data and user_data.role == 'user':
            return RedirectResponse("/")
        else:
            return HTTPException(status_code=302, detail="Not authenticated", headers={"Location": "/login?error=Not+authenticated"})
    else:
        return HTTPException(status_code=302, detail="Not authenticated", headers={"Location": "/login?error=Not+authenticated"})