from django.core.mail import EmailMultiAlternatives
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.simplejson import loads, JSONEncoder


# extend simplejson to allow serializing django queryset objects directly
# Thanks to: chriszweber. https://djangosnippets.org/snippets/2656/
class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)


# Create your views here.
def send_mail(subject, to, template, params):
    from_email = 'no-reply@gobalo.es'
    html_content = render_to_string(template, params)
    '''
    subject, from_email, to = 'Nueva solicitud de amistad', 'no-reply@gobalo.es', friend.email
    html_content = render_to_string('revengeapp/email_sendfriendrequest.html',
                                    {'user': user,
                                     'friend': friend,
                                     })
    '''
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
