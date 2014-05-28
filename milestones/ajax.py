from django.core.mail import EmailMultiAlternatives
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.simplejson import dumps, loads, JSONEncoder

from revengeusers.models import User
from milestones.forms import RevengeMilestoneForm
from revengeapp.models import revengeMilestone
from revengeBook import settings


# extend simplejson to allow serializing django queryset objects directly
# Thanks to: chriszweber. https://djangosnippets.org/snippets/2656/
class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)


@login_required
def add_milestone(request):
    revUser = request.user
    jsonresponse = {'response': "error"}
    data = None
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST
    form = RevengeMilestoneForm(data=data)
    #import ipdb; ipdb.set_trace()
    if form.is_valid():
        friend = User.objects.get(id=request.POST.get("affected", ""))
        revengeMilestone = form.save(user=revUser)
        revUser.add_exp('send_milestone')
        jsonresponse = {'response': True}
        subject, from_email, to = 'Nueva venganza recibida', settings.DEFAULT_FROM_EMAIL, friend.email
        html_content = render_to_string('milestone/email_sendmilestone.html',
                                        {'user': revUser,
                                         'milestone': revengeMilestone,
                                         })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)