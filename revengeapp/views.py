# encoding: utf-8
from datetime import date
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from revengeapp.forms import SignInForm, SignUpForm
from revengeapp.models import revengeCat, revengeExpLog, revengeMilestone, User
# Create your views here.
from django.views.generic.list import ListView


class MilestoneListView(ListView):
    model = revengeMilestone
    template_name = "revengeapp/milestones.html"
    context_object_name = 'milestones'

    def get_queryset(self):
        #import ipdb; ipdb.set_trace()
        return revengeMilestone.objects.filter(Q(owner=self.kwargs['idfriend']) | Q(affected=self.kwargs['idfriend'])).order_by('-milestone_date')

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


def add_friend(request):
    user = request.user
    resultOp = False
    if request.method == 'GET':
        idfriend = request.GET.get("friendId", "")
        if len(idfriend) == 0:
            return HttpResponseRedirect(reverse('RevengePanel'))
        friend = User.objects.get(id=idfriend)
        friend.friends.add(user)
        friend.save()
        resultOp = True
    return render_to_response('revengeapp/add-friend.html', {
                               'friend': friend,
                               'result': resultOp,
                               },
                              context_instance=RequestContext(request))


def index(request):
    data = None
    if request.method == 'POST':
        data = request.POST
    form = SignInForm(data=data)
    if form.is_valid():
        user = form.user
        login(request, user)
        return HttpResponseRedirect(reverse('RevengePanel'))
    return render_to_response('revengeapp/index.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def sign_up(request):
    data = None
    if request.method == 'POST':
        data = request.POST
    form = SignUpForm(data=data)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponseRedirect(reverse('RevengePanel'))
    return render_to_response('revengeapp/sign-up.html',
                              {'form': form, },
                              context_instance=RequestContext(request))


@login_required
def revenge_panel(request):
    actualYear = date.today().year
    user = request.user
    revCats = revengeCat.objects.all()
    for cat in revCats:
        cat.milestones = revengeMilestone.objects.filter(Q(affected=user), Q(cat=cat)).order_by('-milestone_date').count()

    milestones = revengeMilestone.objects.filter(Q(owner=user) | Q(affected=user)).order_by('-milestone_date')
    #import ipdb; ipdb.set_trace()
    for milestone in milestones:
        if milestone.owner == user:
            milestone.tome = True
            milestone.route = 'Para'
        else:
            milestone.tome = False
            milestone.route = 'De'
    return render_to_response('revengeapp/revenge-panel.html', {
                               'friendsList': user.friends.all(),
                               'milestones': milestones,
                               'totalPoints': revCats,
                               },
                              context_instance=RequestContext(request))


@login_required
def revenge_panel_history(request):
    user = request.user
    logs = revengeExpLog.objects.filter(Q(owner=user)).order_by('-log_date')
    return render_to_response('revengeapp/revenge-panel_history.html', {
                               'logs': logs,
                               },
                              context_instance=RequestContext(request))


@login_required
def search_friend(request):
    searchFriend = request.POST.get("searchFriendNavBar","")
    if len(searchFriend) == 0:
        return HttpResponseRedirect(reverse('RevengePanel'))
    friends = User.objects.filter(username__contains=searchFriend).order_by('-username')
    return render_to_response('revengeapp/search-friend.html', {
                               'searchFriend': searchFriend,
                               'searchFriendList': friends,
                               },
                              context_instance=RequestContext(request))


@login_required
def see_profile(request, idfriend):
    if len(idfriend) == 0:
        return HttpResponseRedirect(reverse('RevengePanel'))
    friend = User.objects.get(id=idfriend)
    friend.exp_percet = (float(friend.experience_actual) / float(friend.level.points)) * 100

    totalMilestonesSend = revengeMilestone.objects.filter(owner=friend).count()
    totalMilestonesReveived = revengeMilestone.objects.filter(affected=friend).count()

    revCats = revengeCat.objects.all()
    #import ipdb; ipdb.set_trace()
    milestonesMax = 0
    for cat in revCats:
        cat.milestones = revengeMilestone.objects.filter(Q(affected=friend), Q(cat=cat)).count()
        if milestonesMax < cat.milestones:
            milestonesMax = cat.milestones
    
    for cat in revCats:
        if milestonesMax > 0:
            cat.milestones_percent = int((float(cat.milestones) / float(milestonesMax)) * 100)
        else:
            cat.milestones_percent = 0
    return render_to_response('revengeapp/profile-friend.html', {
                               'friend': friend,
                               'totalPointsCats': revCats,
                               'totalMilestonesSend': totalMilestonesSend,
                               'totalMilestonesReveived': totalMilestonesReveived,
                               },
                              context_instance=RequestContext(request))