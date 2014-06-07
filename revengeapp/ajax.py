from common.views import DjangoJSONEncoder, send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.utils.simplejson import dumps

from revengeusers.models import revengeUser


#TODO: search_friend y search_my_friend could be merged
@login_required
def search_friend(request):
    user = request.user
    jsonresponse = {'response': "error",
                    'friends': []}
    if 'searchFriend' in request.POST:
        searchFriend = request.POST.get("searchFriend")
        SF = User.objects.filter(Q(username__icontains=searchFriend),
                                 ~Q(id=user.id)).order_by('-username')
        #import ipdb; ipdb.set_trace()
        jsonresponse = {
             'response': True,
             'friends': [],
             }
        # Loop to not send all data about an user
        for friend in SF:
            jsonresponse['friends'].append({
                                    'id': friend.pk,
                                    'username': friend.username,
                                    'first_name': friend.first_name,
                                    'last_name': friend.last_name,
                                    'email': friend.email
                                    })

    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)


@login_required
def search_my_friend(request):
    user = request.user
    jsonresponse = {'response': False,
                    'friends': []}
    if 'searchFriend' in request.POST:
        searchFriend = request.POST.get("searchFriend")
        SF = revengeUser.objects.filter(Q(username__icontains=searchFriend),
                                 ~Q(id=user.id),
                                 Q(friends=user)).order_by('-username')
        #import ipdb; ipdb.set_trace()
        jsonresponse = {
             'response': True,
             'friends': [],
             }
        # Loop to not send all data about an user
        for friend in SF:
            jsonresponse['friends'].append({
                                    'id': friend.pk,
                                    'username': friend.username,
                                    'first_name': friend.first_name,
                                    'last_name': friend.last_name,
                                    'email': friend.email
                                    })

    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)


@login_required
def send_friend_request(request):
    user = request.user
    jsonresponse = {'response': False}
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        friendId = request.POST.get("friendId", "")
        if len(friendId) > 0:
            friend = revengeUser.objects.get(id=request.POST.get("friendId", ""))
            send_mail(send_mail='Nueva solicitud de amistad', 
                      to=friend.email, 
                      template='revengeapp/email_sendfriendrequest.html',
                      params={'user': user,
                            'friend': friend,
                    })
            jsonresponse = {'response': True}
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)
