from rest_framework.routers import SimpleRouter
from .views import (UserViewSet)
from django.urls import path, include
from django.urls import path
# from .views import fetch_typeform_responses


 

router = SimpleRouter(trailing_slash=False)
router.register("api/user", UserViewSet, basename="user")



urlpatterns = [
    path("", include(router.urls)),
    path("api/signup", UserViewSet.as_view({"post": "signup"}), name="signup"),
    path("api/login", UserViewSet.as_view({"post": "email_login"}), name="email_login"),
   

]