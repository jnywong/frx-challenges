from django.db import models
from django.contrib.auth.models import User

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