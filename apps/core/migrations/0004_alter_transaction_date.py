# Generated by Django 4.2.1 on 2023-06-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_account_account_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
