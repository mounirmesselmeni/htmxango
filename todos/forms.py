from typing import Any

from crispy_forms.helper import FormHelper
from django import forms

from todos.models import TodoItem


class TodoItemForm(forms.ModelForm):
    title = forms.CharField(max_length=100, min_length=3)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = TodoItem
        fields = ["title"]

    def clean_title(self) -> str:
        title = self.cleaned_data["title"]
        if title.lower() == "error":
            raise forms.ValidationError("You cannot use the word 'error' in the title")
        return title
