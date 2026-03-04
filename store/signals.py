from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart, UserProfile, Wishlist


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user-related objects when new user is created"""
    if created:
        Cart.objects.get_or_create(user=instance)
        UserProfile.objects.get_or_create(user=instance)
        Wishlist.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
