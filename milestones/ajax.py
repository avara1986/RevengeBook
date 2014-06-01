from common.views import DjangoJSONEncoder, send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.simplejson import dumps

from milestones.forms import RevengeMilestoneForm
from revengeapp.models import revengeMilestone
from revengeusers.models import User



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
        send_mail(send_mail='Nueva venganza recibida', 
                  to=friend.email, 
                  template='milestone/email_sendmilestone.html',
                  params={'user': revUser,
                         'milestone': revengeMilestone,
                         })
        jsonresponse = {'response': True}
    json = dumps(jsonresponse, cls=DjangoJSONEncoder)
    return HttpResponse(json)