from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

User = get_user_model()


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20)

    class PaymentsType(models.TextChoices):
        C = "C", _("Cash")
        D = "D", _("Digital")

    type = models.CharField(max_length=1, choices=PaymentsType.choices)

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=32)
    payment_methods = models.ManyToManyField(PaymentMethod, through="AccountMapping")

    def __str__(self):
        return self.name


class AccountMapping(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["payment_method", "office"], name="unique_%(class)s"
            ),
        ]

    payment_method = models.ForeignKey("PaymentMethod", models.CASCADE)
    office = models.ForeignKey("Office", models.CASCADE)
    account = models.ForeignKey("Account", models.CASCADE, related_name="mappers")

    def __str__(self):
        return f"{self.payment_method} - {self.office}"


class Account(models.Model):
    name = models.CharField(max_length=32)
    balance = MoneyField(
        max_digits=settings.MAX_CURRENCY_DIGITS,
        default=0,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Cash(models.Model):
    class Meta:
        verbose_name_plural = "Cash"

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
    office = models.ForeignKey(Office, models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, models.CASCADE)
    account = models.ForeignKey(Account, models.CASCADE)
    amount = MoneyField(max_digits=settings.MAX_CURRENCY_DIGITS)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey("Person", models.CASCADE)

    class Type(models.TextChoices):
        deposit = "deposit", _("Deposit")
        withdrawal = "withdrawal", _("Withdrawal")
        correction = "correction", _("Correction")
        payement = "payement", _("Payement")
        deposit_refund = "deposit_refund", _("Deposit Refund")
        reimbursement = "reimbursement", _("Reimbusement")

    type = models.CharField(max_length=30, choices=Type.choices)
    reason = models.CharField(max_length=256, blank=True)

    details_dump = models.JSONField(default=dict, blank=True)

    def get_absolute_url(self):
        return reverse("transaction-detail", kwargs={"id": self.id})
