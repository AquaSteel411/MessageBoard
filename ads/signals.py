from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Author, Advertisement, Reply
from .utils import send_notifications


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()
        author = Author.objects.create(user=instance)
        author.save()


@receiver(post_save, sender=Reply)
def create_reply(sender, instance, created, **kwargs):
    if created:
        ad = Advertisement.objects.get(id=instance.ad_id)
        owner_ad = User.objects.get(id=ad.author_id)
        user = User.objects.get(id=instance.author.user_id)
        title = f'Новый отклик от игрока {user.username}'
        template = 'email/new_reply.html'
        send_notifications(instance.preview(), instance.pk, title, owner_ad.email,
                           user.email, user.username, template)
