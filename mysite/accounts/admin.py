from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import SignUpForm


@admin.register(User)
class CustomAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "agreement_accepted")}),
        (_("Personal info"), {"fields": ("avatar", "first_name", "last_name", "email", "phone", "date_birth", "about_me")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # save_on_top = True
    # add_form = SignUpForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     actions = []
#     inlines = []
#     list_display = 'pk', 'user', 'first_name', 'last_name', 'bio', 'avatar'
#     list_display_links = 'pk', 'first_name'
#     ordering = 'pk', 'first_name'
#     search_fields = 'first_name', 'email'
#     fieldsets = [
#         (None, {
#             'fields': ('first_name', 'last_name')
#         }),
#         ('Image', {
#             'fields': ('avatar', ),
#         }),
#     ]

#     def description_short(self, obj: Profile) -> str:
#         if len(obj.bio) < 48:
#             return obj.bio
#         return obj.bio[:48] + '...'
