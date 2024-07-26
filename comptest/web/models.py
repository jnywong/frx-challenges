from django.contrib.auth.models import User
from django.db import models, transaction


# Create your models here.
class Submission(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED"
        UPLOADING = "UPLOADING"
        UPLOADED = "UPLOADED"
        CLEARED = "CLEARED"

    # FIXME: Cascade is probably not quite right?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # FIXME: Figure out max_length
    data_uri = models.CharField(max_length=4096)
    # FIXME: Figure out max_length or use IntChoices
    status = models.CharField(choices=Status, default=Status.NOT_STARTED, max_length=16)

    def __str__(self):
        return f"({self.status}) {self.data_uri}"


class Evaluation(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED"
        EVALUATING = "EVALUATING"
        EVALUATED = "EVALUATED"
        HIDDEN = "HIDDEN"
        FAILED = "FAILED"

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    evaluator_state = models.JSONField(default=dict)
    result = models.JSONField(blank=True, null=True)
    # FIXME: Figure out max_length or use IntChoices
    status = models.CharField(choices=Status, default=Status.NOT_STARTED, max_length=16)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.status}) {self.result} {self.submission.data_uri}"


class Team(models.Model):
    name = models.CharField(max_length=1024)
    members = models.ManyToManyField(
        User, through="TeamMembership", related_name="teams"
    )


class TeamMembership(models.Model):
    is_admin = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        # A user can be added to a team only once
        unique_together = ("user", "team")


class Page(models.Model):
    title = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=128, help_text="Slug used to refer to this page's URL")
    order = models.IntegerField(unique=True, help_text="Ordering of this page on the navbar")
    is_home = models.BooleanField(default=False, help_text="Use current page as the home page. Only one page can have this enabled at any given time")
    content = models.TextField(help_text="Markdown specifying the page's content")

    def save(self, *args, **kwargs):
        if not self.is_home:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            Page.objects.filter(is_home=True).update(is_home=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
