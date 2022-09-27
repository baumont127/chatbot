from django import forms
from .models import Ressource, Type_ressource


class RessourceForm(forms.Form):
    lien = forms.URLField(max_length=300, required=False)
    ressource = forms.ModelChoiceField(queryset=None, required=True)
    titre = forms.CharField(max_length=200, required=False)
    key_word = forms.CharField(max_length=100, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ressource'].queryset = Type_ressource.objects.all()
