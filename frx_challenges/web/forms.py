from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_jsonform.forms.fields import JSONFormField
from web.models import Collaborator, Submission, User

from .md import MARKDOWN_RENDERER


class SubmissionForm(forms.ModelForm):
    """Form to create a new submission"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Submit", css_class="form-control btn btn-secondary")
        )

        self.fields["name"] = forms.CharField()
        self.fields["name"].label = "Submission name"
        self.fields["description"] = forms.CharField(
            widget=forms.Textarea(attrs={"rows": 4}), required=False
        )
        self.fields["metadata"] = JSONFormField(
            schema=settings.SITE_SUBMISSION_FORM_SCHEMA
        )
        self.fields["toc_accepted"] = forms.BooleanField(
            label=mark_safe(
                MARKDOWN_RENDERER.renderInline(settings.SITE_SUBMISSION_TOC_LABEL)
            ),
            required=True,
        )

    class Meta:
        model = Submission
        fields = ["name", "description", "metadata", "toc_accepted"]


class UploadForm(forms.Form):
    """Form to upload a version of a submission to be evaluated"""

    def __init__(self, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("upload", args=[self.id])
        self.helper.add_input(
            Submit("submit", "Submit", css_class="form-control btn btn-secondary")
        )

        self.fields["file"] = forms.FileField()
        self.fields["file"].label = False


class AddCollaboratorForm(forms.Form):
    """Form to add a collaborator to a submission"""

    def __init__(self, *args, **kwargs):
        self.submission_id = kwargs.pop("submission_id")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Submit", css_class="form-control btn btn-secondary")
        )

        self.fields["username"] = forms.CharField()
        self.fields["username"].label = "GitHub username"

    def clean(self):
        """
        Validate that the user exists and isn't already a collaborator.
        """
        cleaned_data = super().clean()
        if "username" in cleaned_data:
            try:
                user = User.objects.get(username__iexact=cleaned_data["username"])
                if Collaborator.objects.filter(
                    submission_id=self.submission_id, user_id=user.id
                ).exists():
                    raise forms.ValidationError(
                        "This collaborator is already added to the submission."
                    )
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "User has not logged into this website with their GitHub account."
                )
        return cleaned_data
