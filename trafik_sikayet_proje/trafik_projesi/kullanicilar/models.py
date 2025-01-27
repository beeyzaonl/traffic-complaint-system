from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profil(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    puan = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.kullanici.username} Profili"

@receiver(post_save, sender=User)
def profil_olustur(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(kullanici=instance)

@receiver(post_save, sender=User)
def profil_kaydet(sender, instance, **kwargs):
    instance.profil.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    theme = models.CharField(max_length=20, choices=[('dark', 'Dark'), ('light', 'Light')], default='light')
    language = models.CharField(max_length=20, choices=[('tr', 'Türkçe'), ('en', 'English')], default='tr')

    def __str__(self):
        return f"{self.user.username} UserProfile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class SecuritySettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    two_factor_auth = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} SecuritySettings"


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    issue_notifications = models.BooleanField(default=True)
    comment_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    traffic_alerts = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} NotificationSettings"

class PrivacySettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anonymous_reporting = models.BooleanField(default=True)
    location_access = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} PrivacySettings"
