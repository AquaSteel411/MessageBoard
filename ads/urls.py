from django.urls import path

from .views import (AdvertisementList, AdvertisementDetail, AdvertisementCreate,
                    AdvertisementUpdate, SearchAdvertisement, create_reply,
                    AdvertisementDelete, MyAdList, AdReplyList, ReplyDelete,
                    ReplyDetail, response_to_reply)

urlpatterns = [
    path('', AdvertisementList.as_view(), name='ads_list'),
    path('my_ads', MyAdList.as_view(), name='my_ads'),
    path('my_reply_list', AdReplyList.as_view(), name='my_reply_list'),
    path('<int:pk>', AdvertisementDetail.as_view(), name='ad_detail'),
    path('create/', AdvertisementCreate.as_view(), name='ad_create'),
    path('search/', SearchAdvertisement.as_view(), name='search'),
    path('<int:pk>/update/', AdvertisementUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdvertisementDelete.as_view(), name='ad_delete'),
    path('<int:pk>/create_reply', create_reply, name='create_reply'),
    path('my_reply_list/<int:pk>', ReplyDetail.as_view(), name='reply'),
    path('my_reply_list/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('my_reply_list/<int:pk>/response', response_to_reply, name='response'),
]
