from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import AdvertisementFilter, ReplyFilter
from .forms import AdvertisementForm
from .models import Advertisement, Author, Reply
from django.conf import settings

from .utils import send_notifications


class AdvertisementList(ListView):
    model = Advertisement
    ordering = '-created'
    template_name = 'ads/ads_list.html'
    context_object_name = 'ads_list'
    paginate_by = 10


class MyAdList(ListView):
    model = Advertisement
    ordering = '-created'
    template_name = 'ads/my_ads.html'
    context_object_name = 'my_ads'

    def get_context_data(self, **kwargs):
        """We form a new list consisting only of responses to the user's ads"""
        context = super().get_context_data(**kwargs)
        context['my_ads'] = context['my_ads'].filter(author_id=self.request.user.id)
        return context


class AdReplyList(ListView):
    model = Reply
    ordering = '-created'
    template_name = 'ads/my_reply_list.html'
    context_object_name = 'reply_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """We form a new list consisting only of responses to the user's ads"""
        context = super().get_context_data(**kwargs)
        user = Author.objects.get(user_id=self.request.user.id)
        context['reply_list'] = context['reply_list'].filter(ad__author=user)
        context['filterset'] = self.filterset
        return context


class SearchAdvertisement(ListView):
    model = Advertisement
    ordering = '-created'
    template_name = 'ads/search.html'
    context_object_name = 'ads_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertisementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'ads/ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(ad_id=self.kwargs["pk"])
        return context


class ReplyDetail(DetailView):
    model = Reply
    template_name = 'ads/reply.html'
    context_object_name = 'reply'


class AdvertisementCreate(CreateView):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'ads/ad_edit.html'

    def form_valid(self, form):
        """Autofill the author field"""
        user = self.request.user.id
        form.instance.author = Author.objects.get(user_id=user)
        return super(AdvertisementCreate, self).form_valid(form)


class AdvertisementUpdate(UpdateView):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'ads/ad_edit.html'

    def get(self, request, *args, **kwargs):
        """Overriding the get() method, the ad can only be updated by its creator or superuser"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = request.user
        if not user.is_superuser and self.object.author.user_id != user.id:
            raise Http404('Нет прав на изменение данной записи!')
        return self.render_to_response(context)


class AdvertisementDelete(DeleteView):
    model = Advertisement
    template_name = 'ads/ad_delete.html'
    success_url = reverse_lazy('ads_list')

    def get(self, request, *args, **kwargs):
        """Overriding the get() method, the ad can only be deleted by its creator or superuser"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = request.user
        if not user.is_superuser and self.object.author.user_id != user.id:
            raise Http404('Нет прав на удаление данной записи!')
        return self.render_to_response(context)


class ReplyDelete(DeleteView):
    model = Reply
    template_name = 'ads/reply_delete.html'
    success_url = reverse_lazy('my_reply_list')


@login_required(redirect_field_name='')
def create_reply(request, pk):
    try:
        ad = Advertisement.objects.get(id=pk)
    except:
        raise Http404('Advertisement is not found')

    author = Author.objects.get(user_id=request.user.id)
    ad.reply_set.create(author=author, text=request.POST['text'])
    return HttpResponseRedirect(reverse('ad_detail', args=(ad.pk,)))


@login_required(redirect_field_name='')
def response_to_reply(pk):
    """Acceptance of the response and sending an email to the owner and then deleting the response"""
    try:
        reply = Reply.objects.get(id=pk)
    except:
        raise Http404('Reply is not found')

    try:
        ad = Advertisement.objects.get(id=reply.ad_id)
    except:
        raise Http404('Advertisement is not found')

    title = f'Ответ на {ad.title}'
    user = User.objects.get(id=reply.author.user_id)
    owner_ad = User.objects.get(id=ad.author_id)
    template = 'email/response_to_reply_email.html'

    send_notifications(reply.preview(), ad.id, title, user.email,
                       owner_ad.email, user.username, template)
    reply.delete()
    return HttpResponseRedirect(reverse('my_reply_list'))
