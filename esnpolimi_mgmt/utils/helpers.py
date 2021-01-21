from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.html import format_html
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin


def create_link(link, text):
    return format_html("<a href={link}>{text}</a>", link=link, text=text)


class InlineFormHelper(FormHelper):
    form_method = "get"
    form_class = "form-inline"
    field_template = "bootstrap4/layout/inline_field.html"


class ExportFilterTableView(ExportMixin, SingleTableMixin, FilterView):
    form_helper_class = InlineFormHelper
    export_perm = "export_all"

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        filter_set = filterset_class(**kwargs)
        helper = self.form_helper_class()
        helper.add_input(Submit("filter", "Filter"))
        filter_set.form.helper = helper
        return filter_set
