# Generated by Django 4.2.1 on 2023-06-13 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_transaction_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="sender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender",
                to="core.account",
            ),
        ),
    ]
