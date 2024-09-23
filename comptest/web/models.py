from django.contrib.auth.models import User
from django.db import models, transaction

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=1024)
    members = models.ManyToManyField(
        User, through="TeamMembership", related_name="teams"
    )


class Project(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=2048)
    # FIXME: A default for the team had to be provided
    # but because there was no default team, it was set to None
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="projects",
    )


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


class TeamMembership(models.Model):
    is_admin = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        # A user can be added to a team only once
        unique_together = ("user", "team")


class Page(models.Model):
    class MimeType(models.TextChoices):
        markdown = "text/markdown"
        html = "text/html"

    title = models.CharField(max_length=1024)
    slug = models.SlugField(
        max_length=128, help_text="Slug used to refer to this page's URL"
    )
    order = models.IntegerField(
        unique=True, help_text="Ordering of this page on the navbar"
    )
    is_home = models.BooleanField(
        default=False,
        help_text="Use current page as the home page. Only one page can have this enabled at any given time",
    )
    mimetype = models.CharField(
        default=MimeType.markdown,
        help_text="Mimetype used to render this page",
        max_length=32,
        choices=MimeType
    )

    content = models.TextField(help_text="Markdown specifying the page's content")

    def save(self, *args, **kwargs):
        if not self.is_home:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            Page.objects.filter(is_home=True).update(is_home=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentFile(models.Model):
    """
    Files (like images, object files, etc) to be used when constructing pages
    """
    title = models.CharField(max_length=1024)
    slug = models.SlugField(
        max_length=128, help_text="Slug used to refer to this image", unique=True
    )
    file = models.FileField(upload_to="content-files/%Y/%m/%d/")

    def __str__(self):
        return self.title
