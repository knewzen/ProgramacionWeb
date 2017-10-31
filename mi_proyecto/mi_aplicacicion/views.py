# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.shortcuts import render
from django.db.models import Q
from .forms import TweetModelForm
from .models import Tweet
from .mixin import FormUserNeededMixin

# Create your views here.
def home(request):
    tweets = Tweet.objects.all()
    return render(request, "home.html", context={"msg":"hola django", "tweets":tweets})
class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = "tweets/create_view.html"
    success_url = "admin/"

class TweetDetailView(DetailView):
    template_name = "tweets/tweet_detail.html"
    queryset = Tweet.objects.all()
    def get_object(self):
        id = self.kwargs.get("id")
        print id
        return Tweet.objects.get(id=id)

class TweetListView(ListView):
    template_name = "tweets/tweets_list.html"
    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        print self.request.GET
        query = self.request.GET.get("q",None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs
    #queryset = Tweet.objects.all()

class TweetUpdateView(UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name= "tweets/update_view.html"
    success_url = "/tweet/list"
