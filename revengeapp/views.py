# encoding: utf-8
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from revengeapp.forms import SignInForm, SignUpForm
from revengeapp.models import User, revengeMilestone, revengePointCat
# Create your views here.


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
    user = request.user
    revCats = revengePointCat.objects.all()
    for cat in revCats:
        cat.milestones = revengeMilestone.objects.filter(Q(affected=user), Q(point=cat)).order_by('-milestone_date').count()

    milestones = revengeMilestone.objects.filter(Q(owner=user) | Q(affected=user)).order_by('-milestone_date')
    #import ipdb; ipdb.set_trace()
    for milestone in milestones:
        if milestone.owner == user:
            milestone.tome = True
            milestone.route = 'To'
        else:
            milestone.tome = False
            milestone.route = 'Form'
    return render_to_response('revengeapp/revenge-panel.html', {
                               'friendsList': user.friends.all(),
                               'milestones': milestones,
                               'totalPoints': revCats,
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
    milestones = revengeMilestone.objects.filter(Q(owner=friend) | Q(affected=friend)).order_by('-milestone_date')

    #import ipdb; ipdb.set_trace()
    for milestone in milestones:
        if milestone.owner == friend:
            milestone.tome = True
            milestone.route = 'To'
        else:
            milestone.tome = False
            milestone.route = 'Form'

    totalMilestonesSend = revengeMilestone.objects.filter(owner=friend).count()
    totalMilestonesReveived = revengeMilestone.objects.filter(affected=friend).count()

    revCats = revengePointCat.objects.all()
    milestonesMax = 0
    for cat in revCats:
        cat.milestones = revengeMilestone.objects.filter(Q(affected=friend), Q(point=cat)).count()
        if milestonesMax < cat.milestones:
            milestonesMax = cat.milestones
    for cat in revCats:
        if milestonesMax > 0:
            cat.milestones_percent = (float(cat.milestones) / float(milestonesMax)) * 100
        else:
            cat.milestones_percent = 0
    return render_to_response('revengeapp/profile-friend.html', {
                               'friend': friend,
                               'milestones': milestones,
                               'totalPointsCats': revCats,
                               'totalMilestonesSend': totalMilestonesSend,
                               'totalMilestonesReveived': totalMilestonesReveived,
                               },
                              context_instance=RequestContext(request))