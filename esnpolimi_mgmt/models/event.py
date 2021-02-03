import datetime

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition
from djmoney.models.fields import MoneyField

User = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField()
    referents = models.ManyToManyField(User, related_name="referent_of")

    partecipants = models.ManyToManyField(
        "Person", through="Partecipant", related_name="in_events"
    )
    main_list = models.ManyToManyField(
        "Person", through="MainList", related_name="in_ml"
    )
    waiting_list = models.ManyToManyField(
        "Person", through="WaitingList", related_name="in_wl"
    )

    start_date = models.DateField()
    end_date = models.DateField()
    open_registration_date = models.DateField()
    close_registration_date = models.DateField()

    points = models.DecimalField(max_digits=2, decimal_places=1)

    capacity = models.PositiveSmallIntegerField()
    wl_capacity = models.PositiveSmallIntegerField()

    bando = models.BooleanField()
    externals = models.BooleanField(default=False)

    fee = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS, default=0)
    deposit = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS, default=0)

    optional_info = models.ManyToManyField("Optional")

    class Status(models.TextChoices):
        ready = "ready", _("Ready")
        done = "done", _("Done")
        cancelled = "cancelled", _("Cancelled")

    status = FSMField(choices=Status.choices, default=Status.ready)

    def __str__(self):
        return self.name

    def is_open_at(self, date):
        return self.open_registration_date <= date < self.close_registration_date

    @property
    def is_open(self):
        return self.is_open_at(datetime.date.today())

    @transition(field=status, source=Status.ready, target=Status.done)
    def confirm(self):
        pass

    @transition(field=status, source=Status.ready, target=Status.cancelled)
    def cancel(self):
        pass

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"slug": self.slug})


class MainList(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "event"], name="unique_%(class)s"
            ),
        ]

    person = models.ForeignKey("Person", models.CASCADE)
    event = models.ForeignKey("Event", models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)


class WaitingList(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "event"], name="unique_%(class)s"
            ),
        ]

    person = models.ForeignKey("Person", models.CASCADE)
    event = models.ForeignKey("Event", models.CASCADE)
    position = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)


class Optional(models.Model):
    name = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    place_holder = models.CharField(max_length=256)
    order = models.PositiveSmallIntegerField()

    class Types(models.TextChoices):
        int = "int", _("Integer")
        float = "float", _("Float")
        str = "str", _("String")
        checkbox = "checkbox", _("Checkbox")
        multi_checkbox = "multi_checkbox", _("Multi Checkbox")
        select = "select", _("Select")
        multi_select = "multi_select", _("Multi Select")
        radio = "radio", _("Radio Button")

    type = models.CharField(max_length=16, choices=Types.choices)
    required = models.BooleanField()
    default_value = models.CharField(max_length=256, blank=True)
    choices = models.JSONField(default=list, blank=True)
    meaning = models.JSONField(default=dict, blank=True)


class Partecipant(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "event"], name="unique_%(class)s"
            ),
        ]

    person = models.ForeignKey("Person", models.CASCADE)
    event = models.ForeignKey("Event", models.CASCADE)
    transaction = models.ForeignKey(
        "Transaction", models.CASCADE, related_name="partecipant"
    )
    reimbursement = models.ForeignKey(
        "Transaction",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        default=None,
    )
    deposit_refund = models.ForeignKey(
        "Transaction",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        default=None,
    )

    matricola = models.ForeignKey("Matricola", models.CASCADE, blank=True, null=True)
    esncard = models.ForeignKey("ESNcard", models.CASCADE, blank=True, null=True)

    class Status(models.TextChoices):
        payed = "payed", _("Payed")
        to_reimburse = "to_reimbursed", _("To Be Reimbursed")
        to_refund_deposit = "to_refund_deposit", _("To Refund Deposit")
        refunded = "refunded", _("Refunded")
        reimbursed = "reimbursed", _("Reimbursed")
        done = "done", _("Done")

    status = FSMField(choices=Status.choices, default=Status.payed)

    details_dump = models.JSONField(default=dict, blank=True)
