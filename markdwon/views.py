from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ValidationError
from models import (Document)

from .serializers import (DocumentSerializer)
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self,request,pk=None):
        document = Document.objects.filter(pk=pk, user=request.user).first()
        if not document:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=document, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request,pk=None):
        document = Document.objects.filter(pk=pk, user=request.user).first()
        if not document:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk=None):
        if pk:
            document = Document.objects.filter(pk=pk, user=request.user).first()
            if not document:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        documents = Document.objects.filter(user=request.user)
        serializer = self.serializer_class(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
