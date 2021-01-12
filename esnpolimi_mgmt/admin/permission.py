from django.contrib import admin
from django.contrib.auth.models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(content_type__app_label="auth", content_type__model="permission")
        )

    list_display = [
        "name",
        "content_type",
        "codename",
    ]
    list_filters = ["content_type"]
