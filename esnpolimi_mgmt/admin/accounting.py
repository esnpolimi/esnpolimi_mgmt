from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from esnpolimi_mgmt.models import Account, Cash, Office, PaymentMethod, Transaction


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_balance()

    list_display = [
        "name",
        "balance",
    ]
    readonly_fields = ["balance"]
    search_fields = ["name"]

    def balance(self, obj):
        return obj.balance


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_balance()

    list_display = [
        "name",
        "type",
        "balance",
    ]
    list_filter = ("type",)
    readonly_fields = ["balance"]
    search_fields = ["name", "type"]

    def balance(self, obj):
        return obj.balance


@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = [
        "__str__",
        "balance",
    ]
    list_filter = ("payment_method", "office")
    readonly_fields = ["balance"]
    search_fields = ["office", "payment_method"]
    history_list_display = ["balance"]


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = [
        "note_per_account",
        "quantity",
    ]
    list_select_related = ["account"]
    list_filter = ("note_type", "account")
    ordering = ["account", "note_type"]

    def note_per_account(self, obj):
        return f"{obj.get_note_type_display()} in {obj.account}"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs.select_related("client")
            .select_related("operator")
            .select_related("account")
            .select_related("account__office")
            .select_related("account__payment_method")
        )

    list_display = [
        "type",
        "amount",
        "account",
        "timestamp",
        "operator",
        "client",
        "reason",
    ]
    ordering = ["timestamp"]
    date_hierarchy = "timestamp"
    search_fields = ["reason", "operator", "client"]
    autocomplete_fields = ["client", "operator"]

    list_select_related = ["account", "operator", "client"]
    list_filter = (
        "type",
        "operator",
        "account",
        "account__office",
        "account__payment_method",
    )
