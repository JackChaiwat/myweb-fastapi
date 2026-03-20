from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from api.api import router
from api.users_api import router as user_router
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

# =================
# Models migrations
# =================
import models
from database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="secret123"
)

# =====================
# Register static files
# =====================
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# ========================
# Register admin and auth
# =======================
from admin_auth import AdminAuth
admin = Admin(
    app, 
    engine, 
    templates_dir="templates", 
    authentication_backend=AdminAuth(secret_key='secret123')
)

#
# Routers
#
app.include_router(router)
app.include_router(user_router)

# ===========
# Admin views
# ===========
from admin_view import ProductAdmin, UploadView
admin.add_view(ProductAdmin)
admin.add_view(UploadView)

# upload
from fastapi import UploadFile
from fastapi import status

@app.post("/upload-images")
async def upload_images(files: list[UploadFile]):
    file_path = ''
    i = 1
    for file in files:
        content = await file.read()
        PATH = "D:/IT375/DemoEnv/myweb/static/uploads/"
        with open(PATH + file.filename, "wb") as f:
            f.write(content)
            file_path += f'filename{i}=' + file.filename + '&'
            i += 1
    return RedirectResponse(
        "/admin/upload?i=" + i + '&' + file_path, 
        status_code=status.HTTP_303_SEE_OTHER)


#
# JWT Authentication
#
from jwt_auth import create_token

@app.post("/api/login")
def login(username: str, password: str):
    if username == "admin" and password == "1234":
        token = create_token(username)
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )

