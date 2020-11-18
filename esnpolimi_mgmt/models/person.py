import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_extensions.db.fields import RandomCharField
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
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

    def __str__(self):
        return self.name


class Student(models.Model):
    matricola = models.PositiveIntegerField()
    person = models.ForeignKey(Person, models.CASCADE)
    deprecated_on = models.DateField(blank=True, null=True)
    degree = models.CharField(max_length=256)

    class Location(models.TextChoices):
        LEO = "LEO", _(f"{settings.HOME_UNIVERSITY} - Leonardo")
        BOV = "BOV", _(f"{settings.HOME_UNIVERSITY} - Bovisa")
        OTH = "OTH", _(f"{settings.HOME_UNIVERSITY} - Other location")

    host_university = models.CharField(max_length=3, choices=Location.choices)


class ESNcard(models.Model):
    card_number = models.CharField(max_length=16)
    person = models.ForeignKey(Person, models.CASCADE)
    start_validity = models.DateField()
    end_validity = models.DateField()

    section = models.CharField(max_length=64, default=settings.HOME_SECTION)

    def is_active_at(self, time):
        return self.start_validity <= time < self.end_validity

    @property
    def is_active(self):
        return self.is_active_at(datetime.date.today())
