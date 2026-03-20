from sqladmin.authentication import AuthenticationBackend
from sqladmin.authentication import AuthenticationBackend
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_user_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "password": "$2b$12$KbQiPzR8Zqk9G5W6u4cB3u6KJ9z2k6XkX6y7Y3y7Z7kz8Kj3L9F6W"
    }
}

def get_user(username):
    return fake_user_db.get(username)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


class AdminAuth(AuthenticationBackend):

    async def login(self, request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = get_user(username)

        if user and verify_password(password, user["password"]):
            request.session.update({"user_id": user["id"]})
            return True

        return False

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        return "user_id" in request.session
