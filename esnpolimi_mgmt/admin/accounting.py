from django.contrib import admin

from esnpolimi_mgmt.models import Account, Cash, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "balance",
    ]
    list_filter = ("type",)
    readonly_fields = ["balance"]
    search_fields = ["name"]


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
    list_display = [
        "type",
        "amount",
        "account",
        "timestamp",
        "operator",
        "client",
        "reason",
        "office",
    ]
    ordering = ["timestamp"]
    date_hierarchy = "timestamp"
    search_fields = ["reason", "operator", "client"]
    autocomplete_fields = ["client", "operator"]

    list_select_related = ["account", "operator", "client"]
    list_filter = ("type", "office", "account", "operator")
