from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

admin.site.login = staff_member_required(
    view_func=admin.site.login, login_url="/", redirect_field_name=""
)
