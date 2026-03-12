from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField)
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import datetime


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = 'name',


class SignUpForm(UserCreationForm):
    username = UsernameField(
        label=_("Имя пользователя"),
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": _("*Никнейм"),
                   "autofocus": True}
        ),
        # help_text=_("Обязательное поле. Не более 150 символов")
    )
    email = forms.EmailField(
        label=_("Почта"),
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': _('*Email')}
        ),
    )
    phone = PhoneNumberField(
        region="RU",
        label=_("Номер телефона"),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('*Телефон')}),
    )
    first_name = forms.CharField(
        label=_("Имя"),
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Имя")}),
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Фамилия")}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "placeholder": _("*Пароль")}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "placeholder": _("*Повторите пароль")}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username',
                  'email',
                  'phone',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2')
        # field_classes = {"username": UsernameField}


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(
            attrs={'placeholder': _('Имя пользователя'),
                   "autofocus": True})
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Пароль'),
                   "autocomplete": "current-password"}),
    )


class ProfileEditForm(ModelForm):
    # avatar = forms.ImageField(
    #     required=False,
    # )
    # this_year = datetime.date.today().year
    # date_birth = forms.DateField(
    #     required=False,
    #     widget=forms.SelectDateWidget(
    #         years=tuple(range(this_year-120, this_year-5))
    #     ),
    # )
    # date_birth = forms.DateField(
    #     required=False,
    #    # input_formats=['%d.%m.%Y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d'],
    # )

    class Meta:
        model = get_user_model()
        fields = (
            'avatar',
            'email',
            'phone',
            'first_name',
            'last_name',
            'date_birth',
            'about_me',
        )


class UserEditForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            'avatar',
            'email',
            'phone',
            'first_name',
            'last_name',
            'date_birth',
            'about_me',
        )
