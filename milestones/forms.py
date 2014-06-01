from django import forms
from revengeapp.models import revengeMilestone
from revengeusers.models import User


class RevengeMilestoneForm(forms.ModelForm):
    class Meta:
        model = revengeMilestone

    def save(self, commit=True, user=User):
        milestone = super(RevengeMilestoneForm, self).save(commit=False)
        milestone.owner = user
        user.add_exp('send_milestone')
        if commit:
            return milestone.save()
