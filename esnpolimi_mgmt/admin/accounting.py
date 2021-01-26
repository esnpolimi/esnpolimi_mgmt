from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from esnpolimi_mgmt.models import (
    Account,
    AccountMapping,
    Cash,
    Office,
    PaymentMethod,
    Transaction,
)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = ["name"]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
    ]
    list_filter = ("type",)
    search_fields = ["name", "type"]


@admin.register(AccountMapping)
class AccountMappingAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "account",
    ]
    list_filter = ("payment_method", "office")
    search_fields = ["office", "payment_method"]


@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = [
        "name",
        "balance",
    ]
    readonly_fields = ["balance"]
    search_fields = ["name"]
    history_list_display = ["name", "balance"]


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = [
        "note_type",
        "account",
        "quantity",
    ]
    list_select_related = ["account"]
    list_filter = ("note_type", "account")
    ordering = ["account", "note_type"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "amount",
        "office",
        "payment_method",
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

    list_select_related = ["account", "operator", "client", "office", "payment_method"]
    list_filter = (
        "type",
        "operator",
        "account",
        "payment_method",
        "office",
    )
