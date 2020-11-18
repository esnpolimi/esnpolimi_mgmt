from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from fsm_admin.mixins import FSMTransitionMixin

from esnpolimi_mgmt.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(FSMTransitionMixin, auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username", "name", "is_active", "is_staff", "is_superuser"]
    fsm_field = ["status"]

    def name(self, obj):
        return obj.person.name
