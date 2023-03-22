from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Advertisement, Reply


class AdvertisementFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:

        model = Advertisement
        fields = {
            'title': ['icontains'],
            'category': ['icontains'],
        }


class ReplyFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:

        model = Reply
        fields = {
            'text': ['icontains'],
        }


