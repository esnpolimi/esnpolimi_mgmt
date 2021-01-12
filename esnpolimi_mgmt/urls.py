from django.urls import path

from esnpolimi_mgmt.views import PersonDetailView

urlpatterns = [
    path("person/<str:human_id>", PersonDetailView.as_view(), name="person-detail"),
]
