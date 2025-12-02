# server/views.py

# ====================================================
# Django & DRF imports
# ====================================================
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

# Import your extended Profile model
from accounts.models import Profile


# ====================================================
# User Registration (Signup)
# ====================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """
    Create a new user account.
    Expected fields in request.data:
        - email (string, required)
        - password (string, required)
    Response:
        - Success: 201 with user info + tokens
        - Error: 400 with error message
    """
    email = request.data.get("email")
    password = request.data.get("password")

    # Validate required fields
    if not email or not password:
        return JsonResponse(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for duplicate email
    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": "Email already in use"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user
    user = User.objects.create(
        username=email,
        email=email,
        password=make_password(password)
    )

    # Create associated profile (with optional fields)
    Profile.objects.create(
        user=user,
        name=request.data.get("name", ""),
        company=request.data.get("company", "")
    )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return JsonResponse(
        {
            "message": "Account created successfully",
            "id": user.id,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(access),
        },
        status=status.HTTP_201_CREATED
    )


# ====================================================
# User Profile (View & Update)
# ====================================================
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get or update the authenticated user's profile.
    GET:
        Returns user + profile info
    PUT:
        Update profile fields (name, company)
    """
    user = request.user
    profile = getattr(user, "profile", None)

    # GET profile data
    if request.method == "GET":
        return JsonResponse({
            "id": user.id,
            "email": user.email,
            "last_login": user.last_login,
            "name": profile.name if profile else "",
            "company": profile.company if profile else "",
            "balance": str(profile.balance) if profile else "0.00",
            "created_at": profile.created_at if profile else None,
        })

    # UPDATE profile data
    if request.method == "PUT":
        data = request.data
        if profile:
            profile.name = data.get("name", profile.name)
            profile.company = data.get("company", profile.company)
            profile.save()
        return JsonResponse({"message": "Profile updated successfully"})
