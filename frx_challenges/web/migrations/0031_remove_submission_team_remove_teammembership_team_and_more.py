# Generated by Django 5.1.2 on 2024-11-22 17:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0030_evaluation_evaluator_logs"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="team",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="evaluator_logs",
        ),
        migrations.CreateModel(
            name="Collaborators",
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
                ("is_owner", models.BooleanField()),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="web.submission"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "submission")},
            },
        ),
        migrations.DeleteModel(
            name="Team",
        ),
        migrations.DeleteModel(
            name="TeamMembership",
        ),
    ]