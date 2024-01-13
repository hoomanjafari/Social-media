from django.db.models.signals import post_save
from .models import UserProfileModel
from django.contrib.auth.models import User


def profile_extend_signal(sender, **kwargs):
    if kwargs['created']:
        UserProfileModel.objects.create(user=kwargs['instance'])


post_save.connect(receiver=profile_extend_signal, sender=User)
