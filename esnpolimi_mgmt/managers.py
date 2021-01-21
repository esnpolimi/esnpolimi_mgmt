import datetime

from django.db import models
from django.db.models import BooleanField, OuterRef, Q, Subquery, Sum
from django.db.models import Value as V
from django.db.models.expressions import ExpressionWrapper
from django.db.models.functions import Coalesce


class PersonQuerySet(models.QuerySet):
    def with_valid_esncard(self):
        from esnpolimi_mgmt.models import ESNcard

        subq = ESNcard.objects.with_validity().filter(
            person=OuterRef("pk"), validity=True
        )
        return self.annotate(valid_esncard=Subquery(subq.values("pk")))

    def with_valid_matricola(self):
        from esnpolimi_mgmt.models import Matricola

        subq = Matricola.objects.filter(
            person=OuterRef("pk"), deprecated_on__isnull=True
        )
        return self.annotate(valid_matricola=Subquery(subq.values("pk")))

    def with_last_esncard(self):
        from esnpolimi_mgmt.models import ESNcard

        subq = (
            ESNcard.objects.with_validity()
            .filter(person=OuterRef("pk"))
            .order_by("-start_validity")[:1]
        )
        return self.annotate(
            last_esncard=Subquery(subq.values("pk")),
            has_valid_card=Subquery(subq.values("validity")),
        )

    def with_last_matricola(self):
        from esnpolimi_mgmt.models import Matricola

        subq = Matricola.objects.filter(person=OuterRef("pk")).order_by(
            "-deprecated_on"
        )[:1]
        return self.annotate(last_matricola=Subquery(subq.values("pk")))


class ESNcardQuerySet(models.QuerySet):
    def with_validity_at(self, date):
        return self.annotate(
            validity=ExpressionWrapper(
                Q(start_validity__lte=date) & Q(end_validity__gt=date),
                output_field=BooleanField(),
            )
        )

    def with_validity(self):
        today = datetime.date.today()
        return self.with_validity_at(today)


class MatricolaQuerySet(models.QuerySet):
    def with_points(self):
        return self.annotate(points=Coalesce(Sum("partecipant__event__points"), V(0)))


class PaymentMethodQuerySet(models.QuerySet):
    def with_balance(self):
        return self.annotate(balance=Coalesce(Sum("account__balance"), V(0)))


class OfficeQuerySet(models.QuerySet):
    def with_balance(self):
        return self.annotate(balance=Coalesce(Sum("account__balance"), V(0)))


class AccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("office", "payment_method")
