from django.contrib import admin
from .models import Post, Category
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "status",
        "created_date",
        "updated_date",
        "category",
    )
    list_filter = (
        "created_date",
        "updated_date",
        "status",
        "category",
    )
    search_fields = (
        "author",
        "title",
        "updated_date",
        "created_date",
    )


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
