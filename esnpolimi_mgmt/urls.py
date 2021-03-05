from django.urls import path
from django.views.generic import TemplateView

from esnpolimi_mgmt.views import (
    ErasmusCreateView,
    EventDetailView,
    EventListView,
    PersonDetailView,
    PersonListView,
    TransactionDetailView,
    TransactionListView,
)

urlpatterns = [
    path(
        "logo-page",
        TemplateView.as_view(template_name="external/logo_page.html"),
        name="logo-page",
    ),
    path("person/<str:human_id>", PersonDetailView.as_view(), name="person-detail"),
    path("person", PersonListView.as_view(), name="person-list"),
    path("new-erasmus", ErasmusCreateView.as_view(), name="new-erasmus"),
    path("event/<str:slug>", EventDetailView.as_view(), name="event-detail"),
    path("event", EventListView.as_view(), name="event-list"),
    path(
        "transaction/<int:id>",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path("transaction", TransactionListView.as_view(), name="transaction-list"),
]
