from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="core/frontend/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "signup/",
        views.signup,
        name="signup",
    ),
    path("activate/<str:token>", views.activate_account, name="activate_account"),
    path(
        "resend-activation-email/",
        views.resend_activation_email,
        name="resend_activation_email",
    ),
    path("transfer/", views.transfer_amount, name="transfer_amount"),
    path("deposit/", views.deposit_amount, name="deposit_amount"),
    path("withdraw/", views.withdraw_amount, name="withdraw_amount"),

    path("profile/", views.profile, name="profile"),
]
