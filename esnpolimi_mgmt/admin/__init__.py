from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required

from .person import ESNcardAdmin, MatricolaAdmin, PersonAdmin  # noqa F401

site.login = staff_member_required(
    view_func=site.login, login_url="/", redirect_field_name=""
)
