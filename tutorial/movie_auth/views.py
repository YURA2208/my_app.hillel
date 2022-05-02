from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm, RegisterForm
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegisterSerializer
from rest_framework import status


def sign_in(request, *args, **kwargs):
    ctx = {}
    user = request.user
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            # email = request.POST["email"]

            user = authenticate(username=username, password=password,)

            if user:
                login(request, user)
                return HttpResponse(f"GOOD")
        else:
            form = LoginForm()
        ctx["login_form"] = form
        return render(request, "movie_auth/sign_in.html", ctx)

def sign_up(request, *args, **kwargs):
    ctx = {}
    if request.POST:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            # email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=form.cleaned_data.get["username"],
                                password=form.cleaned_data.get["password1"])
            login(request, user)
            return HttpResponse(f"GOOD")
        else:
            ctx["register_form"] = form
    else:
        form = RegisterForm()
        ctx["register_form"] = form
    return render(request, "movie_auth/sign_up.html", ctx)

def logout_view(request):
    logout(request)
    return HttpResponse("YOU GOT OUT")


class AuthSignIn(ObtainAuthToken):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,ctx={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.create(user=user)
        return Response({"token": token.key,"status":
            {"message": "Register","code": f"{status.HTTP_200} OK"}})


class AuthSignUp(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": {"message": "creation","code": f"{status.HTTP_200} OK"}})
        return Response({"error": serializer.errors,"status": f"{status.HTTP_203}not OK"})


class AuthLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # Дает доступ пользователям которые аутентифицировались. У нас есть "AuthToken",
    # который проверяет, имеется ли в заголовке токен

    def post(self, request, format=None):
        request.user.auth_token.delete()  # Делает удаление токена
        return Response(status=status.HTTP_200) # Возвращает пустой ответ.
        # Сообщает об успешности получения запроса