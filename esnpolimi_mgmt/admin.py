from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _

from esnpolimi_mgmt.models import ESNcard, Person, Student

admin.site.login = staff_member_required(
    view_func=admin.site.login, login_url="/", redirect_field_name=""
)


class ESNcardInline(admin.StackedInline):
    model = ESNcard
    extra = 1


class StudentInline(admin.StackedInline):
    model = Student
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

    inlines = [ESNcardInline, StudentInline]

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
        esncard = obj.valid_esncard
        return esncard.card_number if esncard else None

    def valid_matricola(self, obj):
        mat = obj.valid_matricola
        return mat.matricola if mat else None

    def has_valid_card(self, obj):
        return True if obj.valid_esncard else False

    has_valid_card.boolean = True
