from django import forms
from revengeapp.models import User, revengeMilestone


class RevengeMilestoneForm(forms.ModelForm):

    class Meta:
        model = revengeMilestone

    def save(self, commit=True, user=User):
        milestone = super(RevengeMilestoneForm, self).save(commit=False)
        milestone.owner = user

        if commit:
            return milestone.save()