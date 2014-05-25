from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from milestones.models import revengeMilestone
from revengeusers.models import User


@python_2_unicode_compatible
class revengeExpType(models.Model):
    title = models.CharField(max_length=30,
                               unique=True)
    tag = models.CharField(max_length=30,
                               unique=True)
    points = models.IntegerField(verbose_name=_('Points'))

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class revengeExpLog(models.Model):
    log_date = models.DateTimeField(verbose_name=_("Action date"),
                              auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                          related_name='owner_of_action')
    type = models.ForeignKey(revengeExpType, verbose_name=_('Type action'),
                          related_name='type action',
                          blank=True)
    milestone = models.ForeignKey(revengeMilestone, verbose_name=_('Milestone'),
                          related_name=_('milestone_log'),
                          null=True,
                          blank=True)

    def __str__(self):
        return u'De: %s El %s' % (self.owner.username, self.log_date)
