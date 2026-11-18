from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

    def clean_display_name(self):
        return self.cleaned_data["display_name"].strip()
