# Django Imports
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User # if a custom user model is not created -> most of the time you do not need to create this

# REST Imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# App Imports
from appBetakit.helper.betakitFunction import BetakitFundingScraper, headers

# ===== Create your views here.

# === Installation ===
# add djangorestframework 
# add 'rest-framework' inside settings
# add django-cors-headers
# add 'corsheaders' inside settings
# include CORS_ALLOW_CREDENTIALS=True and CORS_ALLOWED_ORIGINS ip's address for the front end
# SET UP DB: makeMigrations and include spycopg2 for cors-headers

@api_view(['POST'])
@permission_classes([AllowAny])
def start_betakitFunding_analysis(request):
    """Don't forget to await this on the front end
    """
    try:
        target_string = request.data.get('target_string')
        betakit = BetakitFundingScraper(
            header=headers,
            target_string=target_string
        )
        return Response(betakit.filtered_articles, status=status.HTTP_200_OK)
    except:
        return Response({'Error': 'Cannot execute function.'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticates a login. Sets the cookie when logged in.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    account = authenticate(username=email, password=password)
    if account:
        token, created = Token.objects.get_or_create(user=account)
        response = Response({
            'detail': 'Login successful',
            'username': account.username, # Added so the nextjs can use it
            'is_interviewer': account.is_interviewer
        })
        response.set_cookie(
            'token',
            token.key,
            httponly=True,       # The cookie is not accessible via JavaScript
            secure=False,         # The cookie is only sent with HTTPS, False in development
            samesite='Lax'       # Strict or Lax recommended for CSRF protection
        )
        response.set_cookie(
            'username',
            account.username,
            httponly=False,       # The cookie is not accessible via JavaScript
            secure=False,         # The cookie is only sent with HTTPS, False in development
            samesite='Lax'       # Strict or Lax recommended for CSRF protection
        )
        return response
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])    
def register(request):
    """Authenticates a login. Sets the cookie when logged in.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    if user: 
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        response = Response({
                'detail': 'Registration successful.'
            }, status=status.HTTP_201_CREATED)
        response.set_cookie(
                'token',
                token.key,
                httponly=True,       # The cookie is not accessible via JavaScript
                secure=False,         # The cookie is only sent with HTTPS, False in development
                samesite='Lax'       # Strict or Lax recommended for CSRF protection
            )
        response.set_cookie(
                'username',
                user.username,
                httponly=False,       # The cookie is not accessible via JavaScript
                secure=False,         # The cookie is only sent with HTTPS, False in development
                samesite='Lax'       # Strict or Lax recommended for CSRF protection
            )
        return response
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)



