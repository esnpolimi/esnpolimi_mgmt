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
    title = "Has Valid ESNcard"
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return (
            ("Yes", _("Yes")),
            ("No", _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(valid_esncard__isnull=False)
        elif value == "No":
            return queryset.exclude(valid_esncard__isnull=False)
        return queryset


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_valid_esncard().with_valid_matricola()

    inlines = [ESNcardInline, MatricolaInline]

    list_display = [
        "name",
        "human_id",
        "email",
        "country",
        "has_valid_card",
        "valid_esncard",
        "valid_matricola",
    ]
    list_filter = [EsnValidFilter]
    ordering = ["last_modified"]

    readonly_fields = ["valid_esncard", "valid_matricola", "has_valid_card"]

    search_fields = ("name", "email", "human_id", "valid_esncard")

    def valid_esncard(self, obj):
        return obj.valid_esncard

    def valid_matricola(self, obj):
        return obj.valid_matricola

    def has_valid_card(self, obj):
        return True if obj.valid_esncard else False

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
