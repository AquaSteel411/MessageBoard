import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Advertisement, Author


class AdvertisementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False

    class Meta:
        model = Advertisement
        fields = ('title', 'category', 'content')
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title[0].islower() or content[0].islower():
            raise ValidationError(
                "The name and text of the ad must begin with a capital letter"
            )

        if f'<p>{title}</p>' == content:
            raise ValidationError(
                "The ad text cannot match the title"
            )
        return


