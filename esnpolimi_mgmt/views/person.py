import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from esnpolimi_mgmt.forms import AspirantForm, ErasmusForm
from esnpolimi_mgmt.models import Person
from esnpolimi_mgmt.utils.helpers import ExportFilterTableView


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    slug_field = "human_id"
    slug_url_kwarg = "human_id"
    context_object_name = "person"
    template_name = "internal/person_detail.html"


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            "name": ["icontains"],
            "email": ["icontains"],
            "human_id": ["icontains"],
        }

    last_esncard = django_filters.CharFilter(
        field_name="last_esncard", lookup_expr="icontains", label="ESNcard"
    )
    has_valid_card = django_filters.BooleanFilter(
        field_name="has_valid_card", label="Has Valid Card"
    )


class PersonTable(tables.Table):
    class Meta:
        model = Person
        exclude = [
            "id",
            "address",
            "idcard_number",
            "idcard_type",
            "phone_number",
            "last_modified",
        ]
        order_by = "last_modified"

    name = tables.Column("Name", linkify=True)
    last_esncard = tables.Column("Last ESNcard")
    has_valid_card = tables.Column("Valid")


class PersonListView(LoginRequiredMixin, ExportFilterTableView):
    model = Person
    table_class = PersonTable
    filterset_class = PersonFilter
    template_name = "internal/table_filtered.html"

    export_name = "person_list"
    export_perm = "export_person_list"

    def get_queryset(self):
        return super().get_queryset().with_last_esncard()


class ErasmusCreateView(SuccessMessageMixin, CreateView):
    model = Person
    template_name = "external/simple_form.html"
    form_class = ErasmusForm
    success_url = reverse_lazy("logo-page")
    success_message = "Hi %(name)s! Welcome to the ESN family"


class AspirantCreateView(SuccessMessageMixin, CreateView):
    model = Person
    template_name = "external/simple_form.html"
    form_class = AspirantForm
    success_url = reverse_lazy("logo-page")
    success_message = "Hi %(name)s! Welcome to the ESN family"
