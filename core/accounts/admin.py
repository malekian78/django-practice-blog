from django.contrib import admin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = (
        "email",
        "is_active",
    )
    search_fields = ("email",)
    ordering = ("-created_date",)
    fieldsets = (
        (
            "auth info",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": ("is_staff", "is_active", "is_superuser"),
            },
        ),
        (
            "group_permissons",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
