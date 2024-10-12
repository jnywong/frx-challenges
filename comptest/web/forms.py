from django import forms

from .models import SubmissionMetadata


class SubmissionForm(forms.Form):
    """Form to create a new submission"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField()
        self.fields["description"] = forms.CharField()
        if SubmissionMetadata.objects.exists():
            metadata = SubmissionMetadata.objects.latest().items
            for m in metadata:
                self.fields[m] = forms.CharField()


class UploadForm(forms.Form):
    """Form to upload a version of a submission to be evaluated"""

    file = forms.FileField()
