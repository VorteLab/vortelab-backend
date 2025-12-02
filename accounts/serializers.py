from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # includem și email-ul din User
    email = serializers.EmailField(source="user.email", read_only=True)
    last_login = serializers.DateTimeField(source="user.last_login", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "name", "company", "balance", "created_at", "last_login"]
        read_only_fields = ["id", "email", "created_at", "last_login"]
