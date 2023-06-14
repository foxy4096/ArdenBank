from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from .models import Account

from apps.core.models import get_user_model


class AccountCreationForm(UserCreationForm):
    first_name = forms.CharField(
        help_text="Required. 150 characters or fewer.", max_length=150
    )
    last_name = forms.CharField(
        help_text="Required. 150 characters or fewer.", max_length=150
    )
    email = forms.EmailField(help_text="Required. 150 characters or fewer.")

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        help_text="Required. 150 characters or fewer.", max_length=150
    )
    last_name = forms.CharField(
        help_text="Required. 150 characters or fewer.", max_length=150
    )
    email = forms.EmailField(help_text="Required. 150 characters or fewer.")
    username = forms.CharField(disabled=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )
        readonly_fields = ("username",)


class SecurityQuestionForm(forms.ModelForm):
    answer_digest = forms.CharField(
        label="Answer",
        widget=forms.PasswordInput(attrs={"placeholder": "Answer"}),
    )

    class Meta:
        model = Account
        fields = ("security_question", "answer_digest")

class TransferForm(forms.Form):
    amount = forms.DecimalField(label="Amount in $", max_digits=15, decimal_places=2)
    recipient = forms.IntegerField(label="Recipient Account Number")


class DepositOrWithdrawalForm(forms.Form):
    amount = forms.DecimalField(label="Amount in $", max_digits=15, decimal_places=2)
    