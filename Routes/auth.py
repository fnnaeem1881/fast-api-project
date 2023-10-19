from fastapi import FastAPI, Request, HTTPException, Form,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db_config import database, connect_to_database, close_database_connection
from Routes.token_key import generate_session_token, get_user_from_session_token
from datetime import datetime, timedelta, timezone
import pytz

router = APIRouter()

templates = Jinja2Templates(directory="templates")
@router.on_event("startup")
async def startup_db():
    await connect_to_database()

@router.on_event("shutdown")
async def shutdown_db():
    await close_database_connection()


@router.route("/login", methods=["GET", "POST"])
async def login(request: Request):
    error_message = request.query_params.get("error")
    success_message = request.query_params.get("success")
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": error_message, "success":success_message})


@router.post("/login/submit")
async def login(email: str = Form(...), password: str = Form(...)):
    # Assuming you have a users table in your database with username and password columns
    user = await database.fetch_one("SELECT * FROM users WHERE email = :email", values={"email": email})
    if user is None or user["password"] != password:
        return RedirectResponse("/login?error=Invalid+credentials")
    
    session_token = generate_session_token(user) 
    dhaka_tz = pytz.timezone('Asia/Dhaka')

    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    expires = expires.astimezone(dhaka_tz) 
    formatted_expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response = RedirectResponse("/dashboard?success=Login+successfully")
    response.set_cookie(key="session_token", value=session_token, expires=formatted_expires)
    return response

@router.route("/register", methods=["GET", "POST"])
async def render_register(request: Request):
    error_message = request.query_params.get("error")
    success_message = request.query_params.get("success")
    return templates.TemplateResponse("auth/register.html", {"request": request, "error": error_message, "success":success_message})

@router.post("/register/submit")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    email: str = Form(...)
):
    if password != confirm_password:
        return RedirectResponse("/register?error=Passwords+do+not+match")
    query = "INSERT INTO users (username, password, email) VALUES (:username, :password, :email)"
    values = {"username": username, "password": password, "email": email}
    await database.execute(query=query, values=values)

    return RedirectResponse("/login?success=Registration+successfully")
