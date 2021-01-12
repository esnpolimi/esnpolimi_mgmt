from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from fsm_admin.mixins import FSMTransitionMixin

from esnpolimi_mgmt.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(FSMTransitionMixin, UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("User info"), {"fields": ("status", "email", "person")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = [
        "username",
        "person",
        "status",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_select_related = ["person"]
    list_filter = ("status", "is_staff", "is_superuser", "is_active", "groups")
    ordering = ("status",)
    readonly_fields = ["status"]
    search_fields = ("username", "person__name", "email")
    autocomplete_fields = ["person"]

    fsm_field = ["status"]
