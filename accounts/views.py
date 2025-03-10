from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ValidationError
from accounts.models import (User)

from .serializers import (UserLoginSerializer, SignUpUserSerializer, UserSerializer)
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model  

User = get_user_model()  



logger = logging.getLogger(__name__)
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ["post", "get", "put", "patch", ]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = UserSerializer(user)
            response = {
                'success': True,
                'message': 'User Details',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(e)
            response = {
                'success': False,
                'message': e.message
            }    
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
            
    def signup(self, request, *args, **kwargs):
        try:

            serializer = SignUpUserSerializer(data=request.data)
            print('hello')
            if serializer.is_valid():
                print('hello11')

                serializer.save()
                print('hello22')

                response = {
                    'success': True,
                    'message': 'User Created Successfully.',
                    'data': UserSerializer(serializer.instance).data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            logger.error(serializer.errors)
            response = {
                'success': False,
                'message': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(e)
            response = {
                'success': False,
                'message': e.message
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def email_login(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.filter(email=serializer.validated_data.get('email')).first()
                refresh = RefreshToken.for_user(user)
                data = UserSerializer(user).data
                data.update({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
                response = {"success": True, "message": "User Logged in Successfully.",
                            "data": data}
                return Response(response, status=status.HTTP_200_OK)
            logger.error(serializer.errors)
            response = {
                'success': False,
                'message': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(e)
            response = {
                'success': False,
                'message': e.message
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

   