# Generated by Django 5.0.7 on 2024-10-16 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0023_submissionmetadata_instructions"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SubmissionMetadata",
        ),
    ]