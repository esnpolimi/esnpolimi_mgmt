import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from esnpolimi_mgmt.models import Transaction
from esnpolimi_mgmt.utils.helpers import ExportFilterTableView


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    slug_field = "id"
    slug_url_kwarg = "id"
    context_object_name = "transaction"
    template_name = "internal/transaction_detail.html"


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ["account", "timestamp"]

    timestamp = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control", "type": "date"}
        )
    )


class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        exclude = [
            "amount_currency",
            "details_dump",
        ]
        order_by = "timestamp"

    id = tables.Column("ID", linkify=True)
    client = tables.Column("Client", linkify=True)
    operator = tables.Column("Operator", linkify=True)


class TransactionListView(LoginRequiredMixin, ExportFilterTableView):
    model = Transaction
    table_class = TransactionTable
    filterset_class = TransactionFilter
    template_name = "internal/table_filtered.html"

    export_name = "transaction_list"
    export_perm = "export_transaction_list"
