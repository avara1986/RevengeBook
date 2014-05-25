# encoding: utf-8
from django.db.models import Q
from django.views.generic.list import ListView
from milestones.models import revengeMilestone


class MilestoneListView(ListView):
    model = revengeMilestone
    template_name = "revengeapp/milestones.html"
    context_object_name = 'milestones'

    def get_queryset(self):
        #import ipdb; ipdb.set_trace()
        return revengeMilestone.objects.filter(Q(owner=self.kwargs['idfriend'])
               | Q(affected=self.kwargs['idfriend'])).order_by('-milestone_date')

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        #import ipdb; ipdb.set_trace()
        for milestone in context['milestones']:
            milestone.tome = False
            milestone.validate = True
            milestone.returnRevenge = True

            if str(milestone.owner.pk) == self.kwargs['idfriend']:
                milestone.tome = True
                milestone.route = 'Para'
            else:
                milestone.route = 'De'

            if milestone.owner == self.request.user:
                milestone.validate = False
                milestone.returnRevenge = False

            if milestone.affected == self.request.user:
                milestone.validate = False
        return context
