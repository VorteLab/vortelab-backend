from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth (Google, GitHub, etc.)
    path("accounts/", include("allauth.urls")),

    # API-ul tău custom pentru signup/login/profile
    path("api/", include("accounts.urls")),   # 👈 corect
]
