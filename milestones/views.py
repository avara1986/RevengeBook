# encoding: utf-8
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView
from milestones.models import revengeMilestone
from revengeusers.models import revengeUser


class MilestoneListView(ListView):
    model = revengeMilestone
    template_name = "milestones/milestones.html"
    context_object_name = 'milestones'

    def get_queryset(self):
        #import ipdb; ipdb.set_trace()
        return revengeMilestone.objects.filter(Q(milestone=None),
               (Q(owner=self.kwargs['idfriend'])
               | Q(affected=self.kwargs['idfriend']))
                                               ).order_by('-milestone_date')

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        #import ipdb; ipdb.set_trace()
        for milestone in context['milestones']:
            milestone.showMilestone = True
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
            try:
                milestone.contrattack = revengeMilestone.objects.get(milestone=milestone.id)
            except revengeMilestone.DoesNotExist:
                milestone.contrattack = False

            if milestone.affected == self.request.user:
                milestone.validate = False
            else:
                milestone.returnRevenge = False
                if milestone.privacy == '0' and milestone.owner != self.request.user:
                    milestone.showMilestone = False
                if milestone.privacy == '2' and revengeUser.objects.filter(Q(id=self.request.user.id),
                                                (Q(friends=milestone.affected) | Q(friends=milestone.owner))).count() == 0:
                    milestone.showMilestone = False
        return context


@login_required
def milestones_form(request):
    milestone_id = request.GET.get("milid", "")
    milestone = None
    is_return = False
    if milestone_id != '':
        milestone = revengeMilestone.objects.get(id=milestone_id)
        is_return = True
    return render_to_response('milestones/milestone_form.html', {
                               'milestone': milestone,
                               'is_return': is_return,
                               },
                              context_instance=RequestContext(request))
