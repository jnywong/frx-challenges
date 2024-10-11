from django import forms


class SubmissionForm(forms.Form):
    """Form create a new submission"""

    name = forms.CharField()
    description = forms.CharField()
    gh_repo = forms.URLField()


class UploadForm(forms.Form):
    """Form to upload a version of a submission to be evaluated"""

    file = forms.FileField()
