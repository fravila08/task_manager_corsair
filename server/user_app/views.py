from django.contrib.auth import login, authenticate, logout
from .models import AppUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from task_proj.utilies import handle_exceptions
from datetime import datetime, timedelta
from .utilities import CookieAuthentication

def create_time_for_cookie(days=0, minutes=2):
    life_time = datetime.now() + timedelta(days=days, minutes=minutes) # token is valid for 1 week
    format_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return format_time

class RefreshAccessToken(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response("No token present", status=s.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            new_refresh = str(refresh)
            response = Response(
                {"message":"Token refreshed"}, status=s.HTTP_200_OK
            )
            response.set_cookie(
                key='access',
                value=new_access,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=1)
            )
            response.set_cookie(
                key='refresh',
                value=new_refresh,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except TokenError as e:
            return Response(str(e), status=s.HTTP_401_UNAUTHORIZED)

# Create your views here.
class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data
        data['username'] = request.data.get('email')
        new_user = AppUser.objects.create_user(**data)
        try:
            new_user.full_clean()
            new_user.save()
            refresh = RefreshToken.for_user(new_user)
            access = str(refresh.access_token)
            # life_time key value http secure samesite
            response = Response({"email":new_user.email}, status=s.HTTP_201_CREATED)
            response.set_cookie(
                key='access',
                value=access,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=1)
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except Exception as e:
            return Response(e.args, status=s.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data
        data['username'] = request.data.get('email')
        user = authenticate(username=data.get('username'), password=data.get("password"))
        if user:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            response = Response({"email":user.email}, status=s.HTTP_201_CREATED)
            response.set_cookie(
                key='access',
                value=access,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=1)
            )
            response.set_cookie(
                key='refresh',
                value=refresh,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=1)
            )
            return response
        else:
            return Response("No user matching credentials", status=s.HTTP_404_NOT_FOUND)

class UserView(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]


class Info(UserView):
    
    @handle_exceptions
    def get(self, request):
        user = request.user
        return Response({"email":user.email})

class LogOut(UserView):
    
    @handle_exceptions
    def post(self, request):
        user = request.user
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError as e:
                print(str(e))
                pass
        response = Response(f"{user.email} has been logged out")
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response