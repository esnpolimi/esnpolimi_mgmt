from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition


class User(AbstractUser):
    """Default user for ESNPolimi-mgmt."""

    person = models.OneToOneField(
        "esnpolimi_mgmt.Person",
        on_delete=models.PROTECT,
    )
    # limit_choices_to={"univeristy": settings.HOME_UNIVERSITY})

    class Status(models.TextChoices):
        aspirant = "aspirant", _("Aspirant")
        rejected = "rejected", _("Rejected Aspirant")
        member = "member", _("Active Member")
        ex_member = "ex_member", _("Ex Member")
        alumnus = "alumnus", _("Alumnus")

    status = FSMField(choices=Status.choices, default=Status.aspirant)

    @transition(field=status, source=Status.aspirant, target=Status.member)
    def activate(self):
        pass

    @transition(field=status, source=Status.aspirant, target=Status.rejected)
    def reject(self):
        pass

    @transition(field=status, source=Status.rejected, target=Status.aspirant)
    def try_again(self):
        pass

    @transition(field=status, source=Status.member, target=Status.ex_member)
    def deactivate(self):
        pass

    @transition(field=status, source=Status.member, target=Status.alumnus)
    def to_alumnus(self):
        pass

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def name(self):
        return f"{self.first_name} {self.last_name}"
