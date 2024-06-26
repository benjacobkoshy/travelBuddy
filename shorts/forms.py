from django import forms
from .models import CreateVideo

class CreateVideoForm(forms.ModelForm):
    class Meta:
        model = CreateVideo
        fields = ['title', 'video']
