from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse

from .models import SubmissionMetadata


class SubmissionForm(forms.Form):
    """Form to create a new submission"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "submissions-create"
        self.helper.add_input(Submit("submit", "Submit", css_class="form-control"))

        self.fields["name"] = forms.CharField()
        self.fields["description"] = forms.CharField(required=False)
        if SubmissionMetadata.objects.exists():
            metadata = SubmissionMetadata.objects.latest().items
            for m in metadata:
                self.fields[m] = forms.CharField()


class UploadForm(forms.Form):
    """Form to upload a version of a submission to be evaluated"""

    def __init__(self, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("upload", args=[self.id])
        self.helper.add_input(Submit("submit", "Submit", css_class="form-control"))

        self.fields["file"] = forms.FileField()
        self.fields["file"].label = False
