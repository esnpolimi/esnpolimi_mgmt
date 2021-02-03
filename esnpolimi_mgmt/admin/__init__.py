from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from .accounting import (  # noqa F401
    AccountAdmin,
    AccountMappingAdmin,
    CashAdmin,
    TransactionAdmin,
)
from .event import (  # noqa F401
    EventAdmin,
    MainListAdmin,
    OptionalAdmin,
    WaitingListAdmin,
)
from .permission import PermissionAdmin  # noqa F401
from .person import ESNcardAdmin, MatricolaAdmin, PersonAdmin  # noqa F401

site.login = staff_member_required(
    view_func=site.login, login_url=reverse("account_login")
)
