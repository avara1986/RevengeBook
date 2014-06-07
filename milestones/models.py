# encoding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from revengeusers.models import revengeUser

PRIVACY_TYPES = (
        ('0', 'Privado'),
        ('1', 'Público'),
        ('2', 'Amigos'),
    )


@python_2_unicode_compatible
class revengeCat(models.Model):
    title = models.CharField(_('title'), max_length=230, unique=True)
    image = models.ImageField(upload_to="revengePointsCats", blank=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class revengeMilestone(models.Model):
    milestone_date = models.DateTimeField(verbose_name=_("Milestone date"),
                              auto_now_add=True)
    owner = models.ForeignKey(revengeUser, verbose_name=_('Owner'),
                              related_name='owner_of_milestone',
                              blank=True)
    affected = models.ForeignKey(revengeUser, verbose_name=_('Affected'),
                              related_name='affected_of_milestone')

    comment = models.CharField(_('Comment'), max_length=250, blank=True)
    cat = models.ForeignKey(revengeCat, verbose_name=_('Category'))
    milestone = models.ForeignKey("self", verbose_name=_('Milestone contrattack'),
                          related_name=_('milestone_contrattack'),
                          null=True,
                          blank=True)
    privacy = models.CharField(max_length=1, verbose_name=_('Privacidad'),
                                      choices=PRIVACY_TYPES,
                                      default=1)

    def __str__(self):
        return u'De: %s Para: %s El %s' % (self.owner.username,
                              self.affected.username, self.milestone_date)
