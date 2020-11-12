from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Default user for ESNPolimi-mgmt."""

    person = models.OneToOneField(
        "esnpolimi_mgmt.Person",
        on_delete=models.PROTECT,
    )
    # limit_choices_to={"univeristy": settings.HOME_UNIVERSITY})

    # status FSM Aspiring NonActivated Member ExMember Alumno

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def name(self):
        return f"{self.first_name} {self.surname}"
