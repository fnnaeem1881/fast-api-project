from fastapi import FastAPI, Request, HTTPException, Form,APIRouter,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from db_config import database, connect_to_database, close_database_connection
from Routes.token_key import generate_session_token, get_user_from_session_token,get_session_token,get_current_user



admin = APIRouter()

templates = Jinja2Templates(directory="templates")
@admin.on_event("startup")
async def startup_db():
    await connect_to_database()

@admin.on_event("shutdown")
async def shutdown_db():
    await close_database_connection()
    




@admin.route("/dashboard", methods=["GET", "POST"])
async def dashboard(request: Request):
    token=request.cookies.get("session_token")
    user = get_current_user(token) 
    print(f" user: {user}")
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "user": user})