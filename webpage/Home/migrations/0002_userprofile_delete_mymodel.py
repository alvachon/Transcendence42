# Generated by Django 4.2.7 on 2023-11-20 01:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("pseudo", models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name="MyModel",
        ),
    ]
