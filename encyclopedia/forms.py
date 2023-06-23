import html
from django import forms
from django.core.exceptions import ValidationError
from encyclopedia import util


class EntryForm(forms.Form):
    title = forms.CharField(label="title", max_length=30)
    content = forms.CharField(label="content", widget=forms.Textarea)
    is_update = forms.BooleanField(
        initial=False, required=False, widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Code sets title field to readonly if the form is an update form
        initial = kwargs.get("initial", {})
        is_update = initial.get("is_update")

        if is_update:
            self.fields.get("title").widget.attrs["readonly"] = True

    def clean(self):
        """Prevents title duplication if form creates new entry."""
        cleaned_data = super().clean()
        entries = util.list_entries()
        title = cleaned_data.get("title")
        is_update = cleaned_data.get("is_update")

        if title in entries and not is_update:
            raise ValidationError("The title already exists.")

    def clean_content(self):
        """Remove HTML tags from content field."""
        content = self.cleaned_data["content"]
        data = html.escape(content, quote=True)
        return data
