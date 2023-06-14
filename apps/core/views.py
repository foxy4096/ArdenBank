from django.shortcuts import render, redirect
from .utils import default_token_generator, send_activation_email
from .forms import (
    AccountCreationForm,
    SecurityQuestionForm,
    TransferForm,
    DepositOrWithdrawalForm,
    ProfileForm,
)
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def frontpage(request):
    return render(request, "core/frontend/frontpage.html")


def signup(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Account Created Successfully! Please check your inbox for the activation link.",
            )
            login(request, user)
            return redirect("frontpage")
    else:
        form = AccountCreationForm()

    return render(request, "core/frontend/signup.html", {"form": form})


def resend_activation_email(request):
    if request.user.account.is_active:
        messages.error(request, "Your account is already active.")
    else:
        send_activation_email(request.user)
        messages.success(request, "Activation email sent.")

    return redirect("frontpage")


@login_required
def activate_account(request, token):
    if default_token_generator.check_token(request.user, token):
        if request.method == "POST":
            form = SecurityQuestionForm(request.POST)
            if form.is_valid():
                request.user.account.security_question = form.cleaned_data[
                    "security_question"
                ]
                request.user.account.answer_digest = make_password(
                    form.cleaned_data["answer_digest"]
                )
                request.user.account.is_active = True
                request.user.account.save()
                messages.success(request, "Your account has been activated.")
                return redirect("frontpage")
        form = SecurityQuestionForm()
        return render(request, "core/frontend/activate.html", {"form": form})
    messages.error(request, "Invalid activation link.", extra_tags="danger")
    return redirect("frontpage")


@login_required
def deposit_amount(request):
    if request.method == "POST":
        form = DepositOrWithdrawalForm(request.POST)
        if form.is_valid():
            request.user.account.deposit(form.cleaned_data["amount"])
            messages.success(request, "Amount deposited.")
            return redirect("frontpage")
    form = DepositOrWithdrawalForm()
    return render(request, "core/frontend/deposit_amount.html", {"form": form})


@login_required
def transfer_amount(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["recipient"])
            if request.user.account.transfer(
                form.cleaned_data["amount"], form.cleaned_data["recipient"]
            ):
                messages.success(request, "Amount transferred.")
            else:
                messages.error(
                    request,
                    "Transfer failed, Maybe due to insufficient funds or wrong recipient (self-transfer is not supported)",
                    extra_tags="danger",
                )
            return redirect("frontpage")

    form = TransferForm()
    return render(request, "core/frontend/transfer_amount.html", {"form": form})


@login_required
def withdraw_amount(request):
    if request.method == "POST":
        form = DepositOrWithdrawalForm(request.POST)
        if form.is_valid():
            if request.user.account.withdraw(form.cleaned_data["amount"]):
                messages.success(request, "Amount withdrawn.")
            else:
                messages.error(request, "Insufficient funds.", extra_tags="danger")
            return redirect("frontpage")
    form = DepositOrWithdrawalForm()
    return render(request, "core/frontend/withdrawl_amount.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Profile Updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "core/frontend/profile.html", {"pform": form})
