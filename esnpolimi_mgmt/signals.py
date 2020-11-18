from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Person

User = get_user_model()


@receiver(pre_save, sender=User)
def create_person(sender, instance, **kwargs):
    if not hasattr(instance, "person"):
        instance.person = Person.objects.create()
