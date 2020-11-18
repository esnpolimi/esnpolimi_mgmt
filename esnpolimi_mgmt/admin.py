from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from esnpolimi_mgmt.models import Person

admin.site.login = staff_member_required(
    view_func=admin.site.login, login_url="/", redirect_field_name=""
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("name", "email", "human_id")
