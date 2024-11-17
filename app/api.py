from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .user_auth import register_user, authenticate_user

app = FastAPI()

# Templates und statische Dateien einbinden
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/register", response_class=HTMLResponse)
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def post_register(request: Request, username: str = Form(...), password: str = Form(...)):
    result = register_user(username, password)
    if result != "Benutzer erfolgreich registriert":
        return templates.TemplateResponse("register.html", {"request": request, "error": result})
    if result == "success":
        return RedirectResponse(url="/login", status_code=302)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    result = authenticate_user(username, password)
    if result != "Login erfolgreich":
        return templates.TemplateResponse("login.html", {"request": request, "error": result})
    return RedirectResponse(url="/welcome", status_code=302)

@app.get("/welcome", response_class=HTMLResponse)
def welcome_page(request: Request, username: str = ""):
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})