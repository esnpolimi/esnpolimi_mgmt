from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from esnpolimi_mgmt.models import ESNcard, Matricola, Person


class ESNcardInline(admin.StackedInline):
    model = ESNcard
    extra = 1


class MatricolaInline(admin.StackedInline):
    model = Matricola
    extra = 0


class EsnValidFilter(admin.SimpleListFilter):
    title = "ESNcard Validity"
    parameter_name = "valid"

    def lookups(self, request, model_admin):
        return (
            ("Yes", _("Yes")),
            ("No", _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(has_valid_card=True)
        elif value == "No":
            return queryset.exclude(has_valid_card=True)
        return queryset


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_last_esncard().with_last_matricola()

    inlines = [ESNcardInline, MatricolaInline]

    list_display = [
        "name",
        "human_id",
        "email",
        "country",
        "has_valid_card",
        "last_esncard",
        "last_matricola",
    ]
    list_filter = [EsnValidFilter]
    ordering = ["last_modified"]

    readonly_fields = ["last_esncard", "last_matricola", "has_valid_card"]

    search_fields = ("name", "email", "human_id", "last_esncard")

    def last_esncard(self, obj):
        return obj.last_esncard

    def last_matricola(self, obj):
        return obj.last_matricola

    def has_valid_card(self, obj):
        return obj.has_valid_card

    has_valid_card.boolean = True


@admin.register(ESNcard)
class ESNcardAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_validity()

    list_display = [
        "card_number",
        "person",
        "validity",
        "start_validity",
        "end_validity",
    ]
    ordering = ["start_validity"]
    date_hierarchy = "start_validity"
    readonly_fields = ["validity"]
    search_fields = ["card_number"]
    autocomplete_fields = ["person"]

    def validity(self, obj):
        return obj.validity


@admin.register(Matricola)
class MatricolaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_points()

    list_display = [
        "matricola",
        "person",
        "points",
        "degree",
        "host_university",
        "deprecated_on",
    ]
    ordering = ["deprecated_on"]
    date_hierarchy = "deprecated_on"
    readonly_fields = ["points"]
    search_fields = ["matricola"]
    autocomplete_fields = ["person"]

    def points(self, obj):
        return obj.points
