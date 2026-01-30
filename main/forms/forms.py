from django import forms
from django.db.models import Count
from main.models import Voting, VotingOption

class VotingForm(forms.Form):
    option = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        label="Time to pick"
    )
    def __init__(self, *args, **kwargs):

        voting = kwargs.pop('voting', None)
        super().__init__(*args, **kwargs)
        if voting:
            self.fields['option'].queryset = VotingOption.objects.filter(voting=voting).annotate(
                votes_count = Count('vote')
            )
            self.fields['option'].label_from_instance = lambda obj: f"{obj.text} ({obj.votes_count})"


class RegForm(forms.Form):
    pass