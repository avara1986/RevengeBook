from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils.simplejson import dumps, loads, JSONEncoder

from revengeapp.models import User


#extend simplejson to allow serializing django queryset objects directly
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
def search_friend(request):
    jsonresponse = {'response': "error",
                    'friends': []}
    if 'searchFriend' in request.POST:
        searchFriend = request.POST.get("searchFriend")
        SF = User.objects.filter(username=searchFriend).order_by('-username')
        jsonresponse = {
                     'response': True,
                     'friends': SF,
                     }
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)
