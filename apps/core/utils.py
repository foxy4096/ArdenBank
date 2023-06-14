from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


def send_activation_email(user):
    subject = "Welcome to the site, Please confirm your email address to activate your account"
    link = f"{settings.WEBHOST}/bank/activate/{default_token_generator.make_token(user)}"
    text_content = f"Please confirm your email address to activate your account: {link}"
    html_content = render_to_string(
        "core/email/activation.html",
        {"user": user, "activate_link": link},
    )
    email = EmailMultiAlternatives(
        subject, text_content, settings.FROM_EMAIL, [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
