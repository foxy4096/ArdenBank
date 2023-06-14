# Generated by Django 4.2.1 on 2023-06-13 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_transaction_sender"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="branch_code",
        ),
        migrations.AddField(
            model_name="account",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
