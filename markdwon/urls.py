from rest_framework.routers import SimpleRouter
from .views import (DocumentViewSet)
from django.urls import path, include
from django.urls import path
# from .views import fetch_typeform_responses


 

router = SimpleRouter(trailing_slash=False)
router.register("api/document", DocumentViewSet, basename="user")

