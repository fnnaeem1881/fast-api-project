from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from db_config import database, connect_to_database, close_database_connection
from fastapi.staticfiles import StaticFiles
import Routes.auth
import Routes.admin
from Routes.token_key import get_current_user


app = FastAPI()
app.include_router(Routes.auth.router)
app.include_router(Routes.admin.admin)

templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/backend", StaticFiles(directory="templates/assets/backend"), name="assets")



@app.route("/", methods=["GET", "POST"])
async def read_root(request: Request):
    token = request.cookies.get("session_token")
    error_message = request.query_params.get("error")
    success_message = request.query_params.get("success")
    try:
        user = get_current_user(token)
        if user:
            return templates.TemplateResponse("index.html", {"user": user,"request": request, "error": error_message, "success":success_message})
    except  HTTPException as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": error_message, "success":success_message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
