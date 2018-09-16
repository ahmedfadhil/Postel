# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        # if request.method == "POST":
        #     print(request.POST.get("title"))
        #     print(request.POST.get("content"))
        #     message success
        messages.success(request, "Message successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "post_form.html", context)


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
    return render(request, "post_list.html", context)
    # return HttpResponse("<h1>Welcome</h1>")


def post_update(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get("title"))
        instance.save()
        # if request.method == "POST":
        #     print(request.POST.get("title"))
        #     print(request.POST.get("content"))
        #     message success
        messages.success(request, "<a href='#'>item</a> Message was updated!", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }

    # return HttpResponse("<h1>Detail</h1>")

    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "<a href='#'>item</a> Message was successfully deleted!", extra_tags="html_safe")
    return redirect("posts:list")
