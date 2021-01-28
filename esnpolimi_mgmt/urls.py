from django.urls import path

from esnpolimi_mgmt.views import (
    EventDetailView,
    EventListView,
    PersonDetailView,
    PersonListView,
)

urlpatterns = [
    path("person/<str:human_id>", PersonDetailView.as_view(), name="person-detail"),
    path("person", PersonListView.as_view(), name="person-list"),
    path("event/<str:slug>", EventDetailView.as_view(), name="event-detail"),
    path("event", EventListView.as_view(), name="event-list"),
]
