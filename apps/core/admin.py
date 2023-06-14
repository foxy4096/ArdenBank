from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path


class AccountInline(admin.StackedInline):
    model = Account
    fields = [
        "balance",
        "account_number",
        "is_active",
        "security_question",
        "answer_digest",
    ]
    readonly_fields = [
        "balance",
        "account_number",
        "security_question",
        "answer_digest",
    ]
    can_delete = False
    verbose_name_plural = "Accounts"


class UserAdmin(BaseUserAdmin):
    """
    Adding the profile inline in user model admin
    """

    inlines = [
        AccountInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Transaction)
