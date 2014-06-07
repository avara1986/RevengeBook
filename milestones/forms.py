from django import forms
from revengeapp.models import revengeMilestone
from revengeusers.models import revengeUser


class RevengeMilestoneForm(forms.ModelForm):
    class Meta:
        model = revengeMilestone

    def save(self, commit=True, user=revengeUser):
        milestone = super(RevengeMilestoneForm, self).save(commit=False)
        milestone.owner = user
        if not  milestone.milestone:
            user.add_exp('send_milestone')
        else:
            user.add_exp('return_milestone')
        if commit:
            return milestone.save()
