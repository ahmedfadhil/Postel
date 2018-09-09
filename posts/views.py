# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.


def post_create(request):
    return HttpResponse("<h1>Create</h1>")


def post_detail(request, id):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance
    }

    # return HttpResponse("<h1>Detail</h1>")

    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()

    if request.user.is_authenticated():
        context = {
            "object_list": queryset,
            "title": "You're in..."
        }
    else:
        context = {
            "title": "Need to login"
        }
    return render(request, "index.html", context)
    # return HttpResponse("<h1>Welcome</h1>")


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
