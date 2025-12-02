# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    extra = 0


class CustomUserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "username", "is_staff", "is_active")
    ordering = ("id",)
    search_fields = ("email", "username")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    inlines = [ProfileInline]

    # 👉 important: când editezi parola, Django folosește ChangePasswordForm
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            return fieldsets
        return fieldsets


# suprascriem admin-ul default pentru User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "balance", "created_at")
    search_fields = ("user__email", "company")
