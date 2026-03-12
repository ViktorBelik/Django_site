from random import random

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _, ngettext_lazy
from django.views import View
from django.urls import reverse_lazy, reverse
from django.conf import settings
from .forms import (
    GroupForm,
    SignUpForm,
    LoginForm,
    ProfileEditForm,
    UserEditForm,
)


class GroupsListView(UserPassesTestMixin, View):
    def test_func(self):
        my_user = self.request.user
        if my_user.is_superuser:
            return True
        return False

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'accounts/groups_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    success_message = _('Form submission successful.')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        messages.success(
            self.request,
            f'Добро пожаловать, {username}! '
            'Ваш профиль успешно зарегистрирован.'
        )

        # Автоматический вход в аккаунт
        # user = authenticate(
        #     self.request,
        #     username=username,
        #     password=password,
        # )
        # login(request=self.request, user=user)

        return response


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password1')
    #     user = authenticate(
    #         self.request,
    #         username=username,
    #         password=password,
    #     )
    #     login(request=self.request, user=user)
    #     return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE,
                     'form': ProfileEditForm}
    model = get_user_model()

    def post(self, request: HttpRequest):
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            return render(request, self.template_name, {'form': form})

        return redirect(request.path)


class ProfileEditView(UserPassesTestMixin, UpdateView):
    # Только владелец
    def test_func(self):
        my_user = self.request.user
        return self.get_object() == my_user

    # Либо вместо запрашиваемого объекта вернуть профиль самого пользователя
    # my_user = self.request.user
    # def get_object(self, *args, **kwargs):
    #     return my_user

    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')


class UserListView(LoginRequiredMixin, ListView):
    queryset = get_user_model().objects.filter(is_superuser=False).order_by('username')
    context_object_name = 'users'
    template_name = 'accounts/user_list.html'

    def get_context_data(self, **kwargs):
        count = self.queryset.count()
        users_found = ngettext_lazy(
            '1 user',
            '{count} users',
            count
        )
        users_found = users_found.format(count=count)

        context = super().get_context_data(**kwargs)
        context["users_found"] = users_found
        return context


class UserInfoView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    context_object_name = 'x_user'
    template_name = 'accounts/user_info.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}


class UserEditView(UserPassesTestMixin, UpdateView):
    # Только администраторы и владелец
    def test_func(self):
        my_user = self.request.user
        if my_user.is_staff:
            return True
        elif self.get_object() == my_user:
            return True
        return False

    form_class = UserEditForm
    model = get_user_model()
    context_object_name = 'x_user'
    template_name = 'accounts/user_edit.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self) -> str:
        return reverse(
            'accounts:user-info',
            kwargs={'pk': self.object.pk}
        )


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r} + {random()}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')
