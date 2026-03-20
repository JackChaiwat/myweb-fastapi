from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):

    async def login(self, request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == "admin" and password == "1234":
            request.session.update({"token": "admin"})
            return True
        return False


    async def logout(self, request):
        request.session.clear()
        return True


    async def authenticate(self, request):
        token = request.session.get("token")
        if token == "admin":
            return True
        return False
