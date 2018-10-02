# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from urllib import quote_plus
from django.utils import timezone


# Create your views here.
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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

    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }

    # return HttpResponse("<h1>Detail</h1>")

    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name_icontains=query) | Q(
                user__last_name_icontains=query)).distinct()

    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page
    page_request_bar = "page"
    page = request.GET.get(page_request_bar)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "You're in...",
        "page_request_bar": page_request_bar,
        "today": today,
    }

    return render(request, "post_list.html", context)
    # return HttpResponse("<h1>Welcome</h1>")


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "<a href='#'>item</a> Message was successfully deleted!", extra_tags="html_safe")
    return redirect("posts:list")
