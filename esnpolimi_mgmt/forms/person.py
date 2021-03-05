from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from esnpolimi_mgmt.models import Matricola, Person


class ErasmusForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ["creation_time", "idcard_type", "idcard_number"]
        widgets = {
            "birthdate": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    matricola = forms.IntegerField()
    degree = forms.CharField(max_length=256)

    def save(self, commit=True):
        person = super().save(commit=commit)

        _ = Matricola.objects.create(
            matricola=self.cleaned_data["matricola"],
            degree=self.cleaned_data["degree"],
            person=person,
        )

        return person

    @property
    def helper(self):
        helper = FormHelper()
        helper.add_input(Submit("submit", "Submit"))
        return helper
