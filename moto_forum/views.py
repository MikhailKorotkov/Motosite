from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import *
from .utils import *


class ForumHome(DataMixin, ListView):
    model = Motorcycle
    template_name = 'moto_forum/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница Форума')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Motorcycle.objects.filter(is_published=True).select_related('brand')


class ShowPost(DataMixin, DetailView):
    model = Motorcycle
    template_name = 'moto_forum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].category_id)
        return dict(list(context.items()) + list(c_def.items()))


class AboutForum(DataMixin, TemplateView):
    template_name = 'moto_forum/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О Сайте')
        return dict(list(context.items()) + list(c_def.items()))


class AddBike(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'moto_forum/addbike.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(SuccessMessageMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'moto_forum/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class MotoCategory(DataMixin, ListView):
    model = Motorcycle
    template_name = 'moto_forum/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Motorcycle.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('brand', 'category')


def pageNotFound(request, exception):
    return render(request, 'moto_forum/pagenotfound.html', {'exception': exception})


def archieve(request, year):
    if len(str(year)) < 4 or int(year) > 2021:
        raise Http404()
    if int(year) < 1999:
        return redirect('home', permanent=True)

    return HttpResponse(f'Архив {year} года')
