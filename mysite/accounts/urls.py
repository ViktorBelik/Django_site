from django.urls import path
from .views import (
    GroupsListView,
    SignUpView,
    MyLoginView,
    MyLogoutView,
    ProfileView,
    ProfileEditView,
    UserListView,
    UserInfoView,
    UserEditView,
    FooBarView,
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
)


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path('groups/', GroupsListView.as_view(), name='groups_list'),

    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/<uuid:pk>/edit/', ProfileEditView.as_view(), name="profile-edit"),

    path('users/', UserListView.as_view(), name="user-list"),
    path('users/<uuid:pk>/', UserInfoView.as_view(), name="user-info"),
    path('users/<uuid:pk>/edit', UserEditView.as_view(), name="user-edit"),

    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
]
