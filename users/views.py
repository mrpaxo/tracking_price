from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer ,UserSigninSerializer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from users.authentication import expires_in, token_expire_handler


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
    signin_serializer = UserSigninSerializer(data = request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)

    user = authenticate(
            username = signin_serializer.data['username'],
            password = signin_serializer.data['password'] 
        )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
        
    #TOKEN STUFF
    token, _ = Token.objects.get_or_create(user = user)
    
    #token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)     # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response({
        'username': user.username, 
        'expires_in': expires_in(token),
        'access_token': token.key,
        'timestamp':token.created
    }, status=HTTP_200_OK)

@api_view(["GET"])
def user_info(request):
    return Response({
        'user': request.user.username,
        'expires_in': expires_in(request.auth)
    }, status=HTTP_200_OK)

@api_view(["GET"])
def logout(request):
    if request.auth:
        Token.objects.get(key = request.auth).delete()
        return Response({'detail': "sesion cerrada con exito"}, status=HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)