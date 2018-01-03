from django.db import models
from django.dispatch import receiver


class User(models.Model):
    mattermost_id = models.CharField(max_length=30, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    heart = models.IntegerField(default=0)
    quota = models.IntegerField(default=100)


@receiver(models.signals.post_save, sender=User)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        Log.objects.create(user=instance, message="Account creation.")


class Log(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
