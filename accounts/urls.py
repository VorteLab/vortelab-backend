from django.urls import path
from .views import signup, signin, profile

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("profile/", profile, name="profile"),  # 👈 asta adaugă ruta
]
