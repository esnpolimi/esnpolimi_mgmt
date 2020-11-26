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
        from esnpolimi_mgmt.models import Student

        subq = Student.objects.filter(person=OuterRef("pk"), deprecated_on__isnull=True)
        return self.annotate(valid_matricola=Subquery(subq.values("pk")))


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


class StudentQuerySet(models.QuerySet):
    def with_points(self):
        return self.annotate(points=Coalesce(Sum("partecipant__event__points"), V(0)))
