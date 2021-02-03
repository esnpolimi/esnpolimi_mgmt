import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from esnpolimi_mgmt.models import Event
from esnpolimi_mgmt.utils.helpers import ExportFilterTableView


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "event"
    template_name = "event-detail.html"


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {"name": ["icontains"], "status": ["exact"]}


class EventTable(tables.Table):
    class Meta:
        model = Event
        exclude = [
            "id",
            "slug",
            "description",
            "fee_currency",
            "wl_capacity",
            "deposit",
            "deposit_currency",
            "optionals",
        ]
        order_by = "open_registration_date"

    name = tables.Column("Name", linkify=True)


class EventListView(LoginRequiredMixin, ExportFilterTableView):
    model = Event
    table_class = EventTable
    filterset_class = EventFilter
    template_name = "table_filtered.html"

    export_name = "event_list"
    export_perm = "export_event_list"
