from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords


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
        l = "0.50", _("0.50€")  # noqa E741
        I = "1", _("1€")  # noqa E741
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


class Transaction(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["timestamp", "account"]),
        ]

    timestamp = models.DateTimeField(default=timezone.now)
    account = models.ForeignKey(Account, models.PROTECT)
    amount = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS)
    operator = CurrentUserField()
    client = models.ForeignKey("Person", models.CASCADE)

    class Type(models.TextChoices):
        payement = "payement", _("Leonardo")
        deposit_refund = "deposit_refund", _("Bovisa")
        reimbursement = "reimbursement", _("Other location")
        correction = "correction", _("Correction")
        withdrawal = "withdrawal", _("Withdrawal")

    type = models.CharField(max_length=30, choices=Type.choices)
    reason = models.CharField(max_length=256, blank=True)

    class Office(models.TextChoices):
        LEO = "LEO", _("Leonardo")
        BOV = "BOV", _("Bovisa")
        OTH = "OTH", _("Other location")

    office = models.CharField(max_length=3, choices=Office.choices)

    details_dump = models.JSONField(default=dict)
