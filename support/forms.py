from django import forms
from .models import Demande, Utilisateur

class AffectationAgentForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['agent']

    def __init__(self, *args, **kwargs):
        super(AffectationAgentForm, self).__init__(*args, **kwargs)
        agents = Utilisateur.objects.filter(profil__libelle="AGENT")
        self.fields['agent'].queryset = agents
        self.fields['agent'].label = "Sélectionner un agent"
        self.fields['agent'].empty_label = "Sélectionner un agent"

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['description', 'service']
