from django.core.mail import EmailMultiAlternatives
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.simplejson import dumps, loads, JSONEncoder

from revengeapp.forms import RevengeMilestoneForm, AddFriendForm
from revengeapp.models import User, revengeMilestone, revengePoint


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


@login_required
def add_milestone(request):
    user = request.user
    jsonresponse = {'response': "error"}
    data = None
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST
    form = RevengeMilestoneForm(data=data)
    if form.is_valid():
        friend = User.objects.get(id=request.POST.get("friendId", ""))
        point = revengePoint.objects.get(id=request.POST.get("point", ""))
        obRevengeMilestone = revengeMilestone.objects.create(owner=user,
                                                 affected=friend, point=point)
        obRevengeMilestone.comment = request.POST.get("comment", "")
        obRevengeMilestone.save()
        jsonresponse = {'response': True}
        subject, from_email, to = 'Nueva venganza recibida', 'no-reply@gobalo.es', friend.email
        html_content = render_to_string('revengeapp/email_sendmilestone.html', 
                                        {'user':user,
                                         'milestone': obRevengeMilestone,
                                         })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)


#TODO: search_friend y search_my_friend could be merged
@login_required
def search_friend(request):
    jsonresponse = {'response': "error",
                    'friends': []}
    if 'searchFriend' in request.POST:
        searchFriend = request.POST.get("searchFriend")
        SF = User.objects.filter(username__contains=searchFriend).order_by('-username')
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
    jsonresponse = {'response': "error",
                    'friends': []}
    if 'searchFriend' in request.POST:
        searchFriend = request.POST.get("searchFriend")
        SF = User.objects.filter(username__contains=searchFriend).order_by('-username')
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