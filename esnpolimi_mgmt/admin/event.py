from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from esnpolimi_mgmt.models import Event, MainList, Optional, Partecipant, WaitingList


@admin.register(MainList)
class MainListAdmin(admin.ModelAdmin):
    list_display = [
        "person",
        "event",
        "timestamp",
        "confirmed",
    ]
    list_filter = ("event",)
    date_hierarchy = "timestamp"
    ordering = ["timestamp"]
    search_fields = ["person", "event"]
    autocomplete_fields = ["person", "event"]


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = [
        "person",
        "event",
        "timestamp",
        "position",
    ]
    list_filter = ("event",)
    date_hierarchy = "timestamp"
    ordering = ["timestamp"]
    search_fields = ["person", "event"]
    autocomplete_fields = ["person", "event"]


@admin.register(Event)
class EventAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "start_date",
        "end_date",
        "open_registration_date",
        "close_registration_date",
        "points",
        "capacity",
        "bando",
        "externals",
        "fee",
        "deposit",
        "status",
    ]
    ordering = ["start_date"]
    date_hierarchy = "start_date"
    search_fields = ["name"]
    list_filter = ("bando", "externals", "status")

    filter_horizontal = ["referents"]

    fsm_field = ["status"]


@admin.register(Optional)
class OptionalAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "label",
        "place_holder",
        "order",
        "type",
        "required",
        "default_value",
        "choices",
        "meaning",
    ]
    ordering = ["id", "order"]
    search_fields = ["name"]
    list_filter = ("type", "required")


@admin.register(Partecipant)
class PartecipantAdmin(admin.ModelAdmin):
    list_display = [
        "partecipation",
        "matricola",
        "esncard",
        "status",
    ]
    ordering = ["transaction__timestamp"]
    date_hierarchy = "transaction__timestamp"
    search_fields = ["person", "event"]
    autocomplete_fields = ["person", "event"]

    list_select_related = ["transaction"]
    list_filter = ("status",)

    def partecipation(self, obj):
        return f"{obj.person} in {obj.event}"
