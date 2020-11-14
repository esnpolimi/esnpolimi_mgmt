import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_currentuser.db.models import CurrentUserField
from django_extensions.db.fields import RandomCharField
from django_fsm import FSMField, transition
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    human_id = RandomCharField(length=4, unique=True, lowercase=False)

    class Gender(models.TextChoices):
        M = "M", _("Male")
        F = "F", _("Female")
        O = "O", _("Other")  # noqa: E741

    gender = models.CharField(max_length=1, choices=Gender.choices)
    birthdate = models.DateField()
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


class Student(models.Model):
    matricola = models.PositiveIntegerField()
    person = models.ForeignKey(Person, models.CASCADE)
    deprecated = models.BooleanField(default=False)

    class Location(models.TextChoices):
        LEO = "LEO", _(f"{settings.HOME_UNIVERSITY} - Leonardo")
        BOV = "BOV", _(f"{settings.HOME_UNIVERSITY} - Bovisa")
        OTH = "OTH", _(f"{settings.HOME_UNIVERSITY} - Other location")

    host_university = models.CharField(max_length=3, choices=Location.choices)

    degree = models.CharField(max_length=256)


class ESNcard(models.Model):
    card_number = models.CharField(max_length=12)
    person = models.ForeignKey(Person, models.CASCADE)
    start_validity = models.DateField()
    end_validity = models.DateField()

    section = models.CharField(max_length=64, default=settings.HOME_SECTION)

    def is_active_at(self, time):
        return self.start_validity <= time < self.end_validity

    @property
    def is_active(self):
        return self.is_active_at(datetime.date.today())


class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = CurrentUserField(on_delete=models.SET_NULL)

    start_date = models.DateField()
    end_date = models.DateField()
    signup_open = models.DateField()
    signup_close = models.DateField()

    points = models.DecimalField(max_digits=2, decimal_places=1)

    capacity = models.PositiveSmallIntegerField()
    wl_capacity = models.PositiveSmallIntegerField()

    bando = models.BooleanField()
    externals = models.BooleanField(default=False)

    fee = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS, blank=True, default=0)
    deposit = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS, blank=True, default=0)

    class Status(models.TextChoices):
        ready = "ready", _("Ready")
        done = "done", _("Done")
        cancelled = "cancelled", _("Cancelled")

    status = FSMField(choices=Status.choices, default=Status.ready)

    def is_open_at(self, time):
        return self.signup_open <= time < self.signup_close

    @property
    def is_open(self):
        return self.is_open_at(datetime.date.today())

    @transition(field=status, source=Status.ready, target=Status.done)
    def confirm(self):
        """Cannot refund anymore."""
        pass

    @transition(field=status, source=Status.ready, target=Status.cancelled)
    def cancel(self):
        """Start refund of all partecipants (not referents)."""
        pass


class MainList(models.Model):
    person = models.ForeignKey(Person, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)


class WaitingList(models.Model):
    person = models.ForeignKey(Person, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    position = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)


class Account(models.Model):
    name = models.CharField(max_length=20)

    class PaymentsType(models.TextChoices):
        C = "C", _("Cash")
        D = "D", _("Digital")

    type = models.CharField(max_length=1, choices=PaymentsType.choices)
    balance = MoneyField(
        max_digits=settings.MAX_CURRENCY_DIGITS,
        default=0,
    )
    history = HistoricalRecords()


class Cash(models.Model):
    account = models.ForeignKey(Account, models.CASCADE)

    class Note(models.TextChoices):
        i = "0.01", _("0.01€")
        ii = "0.02", _("0.02€")
        v = "0.05", _("0.05€")
        x = "0.10", _("0.10€")
        xx = "0.20", _("0.20€")
        l = "0.50", _("0.50€")  # noqa: E741
        I = "1", _("1€")  # noqa: E741
        II = "2", _("2€")
        V = "5", _("5€")
        X = "10", _("10€")
        XX = "20", _("20€")
        L = "50", _("50€")
        C = "100", _("100€")
        CC = "200", _("200€")
        D = "500", _("500€")

    note_type = models.CharField(max_length=4, choices=Note.choices)
    quantity = models.PositiveSmallIntegerField(default=0)
