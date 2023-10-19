from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from db_config import database, connect_to_database, close_database_connection
from fastapi.staticfiles import StaticFiles
import Routes.auth
import Routes.admin


app = FastAPI()
app.include_router(Routes.auth.router)
app.include_router(Routes.admin.admin)

templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")


user_route = APIRouter()
admin_route = APIRouter()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    error_message = request.query_params.get("error")
    success_message = request.query_params.get("success")
    return templates.TemplateResponse("index.html", {"request": request, "error": error_message, "success":success_message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
