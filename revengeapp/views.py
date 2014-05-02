# encoding: utf-8
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from revengeapp.forms import SignInForm, SignUpForm
from revengeapp.models import User, revengeMilestone
# Create your views here.


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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=request.POST.get("username", ""))
            user.email = request.POST.get("email", "")
            user.password = request.POST.get("password", "")
            user.save()
    else:
        form = SignUpForm()

    return render_to_response('revengeapp/register.html',
                              {'form': form, },
                              context_instance=RequestContext(request))


@login_required
def revenge_panel(request):
    user = request.user

    milestones = revengeMilestone.objects.filter(owner=user).order_by('-milestone_date')
    return render_to_response('revengeapp/revenge-panel.html', {
                               'friendsList': user.friends.all(),
                               'milestones': milestones,
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
def see_profile(request):
    pass
