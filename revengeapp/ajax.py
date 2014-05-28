from django.core.mail import EmailMultiAlternatives
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.simplejson import dumps, loads, JSONEncoder

from revengeusers.models import User


# extend simplejson to allow serializing django queryset objects directly
# Thanks to: chriszweber. https://djangosnippets.org/snippets/2656/
class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)


@login_required
def add_friend(request):
    jsonresponse = {'response': "error"}
    if 'addFriendID' in request.POST:
        friend = User.objects.get(id=request.POST.get("addFriendID"))
        user = User.objects.get(id=request.session['member_id'])
        user.friends.add(friend)
        user.save()
        jsonresponse = {'response': "ok"}
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)


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
        SF = User.objects.filter(Q(username__icontains=searchFriend),
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
            friend = User.objects.get(id=request.POST.get("friendId", ""))
            jsonresponse = {'response': True}
            subject, from_email, to = 'Nueva solicitud de amistad', 'no-reply@gobalo.es', friend.email
            html_content = render_to_string('revengeapp/email_sendfriendrequest.html',
                                            {'user': user,
                                             'friend': friend,
                                             })
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            jsonresponse = {'response': True}
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)
