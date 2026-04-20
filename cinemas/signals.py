from django.db.models.signals import pre_save
from django.dispatch import receiver

from cinemas.models import Screen


@receiver(pre_save, sender=Screen)
def check_screen_number_to_cinema(sender, **kwargs):
    print(f"Finished operations, {kwargs}")
