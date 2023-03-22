from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Author, Advertisement, Reply


class AdvertisementAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Advertisement
        fields = '__all__'


class AdvertisementAdmin(admin.ModelAdmin):
    form = AdvertisementAdminForm


admin.site.register(Author)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Reply)
