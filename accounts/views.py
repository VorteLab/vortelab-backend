from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import Profile

# ---------------------
# Signup (register new account)
# ---------------------
@api_view(["POST"])
def signup(request):
    email = request.data.get("email", "").strip().lower()
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")
    company = request.data.get("company", "").strip()
    name = request.data.get("name", "").strip()

    if not email or not password1 or not password2 or not name:
        return Response(
            {"error": "Name, email, and both passwords are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if password1 != password2:
        return Response(
            {"error": "Passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(password1) < 10:
        return Response(
            {"error": "Password must be at least 10 characters long"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    with transaction.atomic():
        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password1),
            first_name=first_name,
            last_name=last_name,
        )

        profile = user.profile
        profile.company = company or None
        profile.balance = Decimal("0.99")
        profile.name = name
        profile.save()

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
        },
        status=status.HTTP_201_CREATED,
    )


# ---------------------
# Signin (classic login)
# ---------------------
@api_view(["POST"])
def signin(request):
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"error": "Account is disabled"},
            status=status.HTTP_403_FORBIDDEN,
        )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
        },
        status=status.HTTP_200_OK,
    )
# ---------------------
# Profile (view & update)
# ---------------------
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    prof = getattr(user, "profile", None)

    # GET → return user info
    if request.method == "GET":
        return Response({
            "id": user.id,
            "email": user.email,
            "name": prof.name if prof else "",
            "company": prof.company if prof else "",
            "balance": str(prof.balance) if prof else "0.00",
            "created_at": prof.created_at if prof else None,
            "last_login": user.last_login,
        })

    # PUT → update profile
    if request.method == "PUT":
        data = request.data
        if prof:
            prof.name = data.get("name", prof.name)
            prof.company = data.get("company", prof.company)
            prof.save()
        return Response({"message": "Profile updated successfully"})