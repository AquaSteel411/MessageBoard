from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Advertisement(models.Model):
    CATEGORIES = [
        ('Tank', 'Танк'),
        ('Healer', 'Хил'),
        ('DD', 'ДД'),
        ('Trader', 'Торговец'),
        ('GM', 'Гильдмастер'),
        ('QG', 'Квестгивер'),
        ('BLACKSMITH', 'Кузнец'),
        ('Tanner', 'Кожевник'),
        ('Potions master', 'Зельевар'),
        ('Spell master', 'Мастер заклинаний')
    ]

    author = models.ForeignKey(Author, models.CASCADE)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=16, choices=CATEGORIES)
    created = models.DateTimeField(auto_now_add=True)
    content = CKEditor5Field(config_name='extends')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Reply(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, models.CASCADE)
    ad = models.ForeignKey(Advertisement, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

    def preview(self):
        return self.text[:64]
