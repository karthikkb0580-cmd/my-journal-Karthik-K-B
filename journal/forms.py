from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "subtitle", "body", "categories", "is_published"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 8}),
            "categories": forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("The title must contain at least 3 characters.")
        return title

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if len(body) < 10:
            raise forms.ValidationError("Please write at least 10 characters in the article.")
        return body
