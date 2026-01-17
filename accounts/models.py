from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GOAL_CHOICES = [
        ('DIET', 'Lose Weight / Diet'),
        ('GAIN', 'Gain Fat / Muscle'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=10, default='Not Specified')
    weight = models.FloatField(help_text="in kg", default=60.0)
    height = models.FloatField(help_text="in cm", default=170.0)
    goal = models.CharField(max_length=4, choices=GOAL_CHOICES, default='DIET')

    def __str__(self):
        return f'{self.user.username} Profile'

# Signals to automatically create profile when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()