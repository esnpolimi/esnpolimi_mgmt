import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_extensions.db.fields import RandomCharField
from phonenumber_field.modelfields import PhoneNumberField

from esnpolimi_mgmt.managers import ESNcardQuerySet, MatricolaQuerySet, PersonQuerySet


class Person(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["human_id"]),
        ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    human_id = RandomCharField(length=4, unique=True, uppercase=True)

    class Gender(models.TextChoices):
        M = "M", _("Male")
        F = "F", _("Female")
        O = "O", _("Other")  # noqa E741

    gender = models.CharField(max_length=1, choices=Gender.choices)
    birthdate = models.DateField(null=True)
    university = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    country = CountryField()
    address = models.CharField(max_length=256)

    idcard_number = models.CharField(max_length=20)
    idcard_type = models.CharField(
        max_length=3,
    )  # choices=IDCARD_TYPES)

    creation_time = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    objects = PersonQuerySet.as_manager()

    def __str__(self):
        return self.name

    def last_esncard(self):
        return self.esncard_set.latest()

    def has_valid_card(self):
        return self.last_esncard().is_valid()

    def last_matricola(self):
        return self.matricola_set.latest()

    def get_absolute_url(self):
        return reverse("person-detail", kwargs={"human_id": self.human_id})


class Matricola(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["matricola"]),
        ]
        get_latest_by = "deprecated_on"
        verbose_name_plural = "Matricole"

    matricola = models.PositiveIntegerField(primary_key=True)
    person = models.ForeignKey(Person, models.CASCADE)
    deprecated_on = models.DateField(blank=True, null=True)
    degree = models.CharField(max_length=256)

    class Location(models.TextChoices):
        LEO = "LEO", _(f"{settings.HOME_UNIVERSITY} - Leonardo")
        BOV = "BOV", _(f"{settings.HOME_UNIVERSITY} - Bovisa")
        OTH = "OTH", _(f"{settings.HOME_UNIVERSITY} - Other location")

    host_university = models.CharField(max_length=3, choices=Location.choices)

    objects = MatricolaQuerySet.as_manager()

    def __str__(self):
        return str(self.matricola)


class ESNcard(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["card_number"]),
        ]
        get_latest_by = "start_validity"
        verbose_name = "ESNcard"
        verbose_name_plural = "ESNcards"

    card_number = models.CharField(max_length=16, primary_key=True)
    person = models.ForeignKey(Person, models.CASCADE)
    start_validity = models.DateField()
    end_validity = models.DateField()

    section = models.CharField(max_length=64, default=settings.HOME_SECTION)

    objects = ESNcardQuerySet.as_manager()

    def __str__(self):
        return str(self.card_number)

    def is_valid_at(self, time):
        return self.start_validity <= time < self.end_validity

    @property
    def is_valid(self):
        return self.is_valid_at(datetime.date.today())
