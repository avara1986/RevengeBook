from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class revengeCat(models.Model):
    title = models.CharField(_('title'), max_length=230, unique=True)
    image = models.ImageField(upload_to="revengePointsCats", blank=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class revengeLvl(models.Model):
    title = models.CharField(max_length=30,
                               unique=True)
    points = models.IntegerField(verbose_name=_('Points'),
                                 default=1)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class User(AbstractUser):
    friends = models.ManyToManyField("self", verbose_name=_('Friends'),
                                    related_name='friends',
                                    null=True,
                                    blank=True)
    avatar = models.ImageField(upload_to="avatars", verbose_name=_('Avatar'),
                                    default='avatars/default/default_avatar.jpg',
                                    null=True,
                                    blank=True)
    experience_total = models.IntegerField(verbose_name=_('Total Experience'),
                                           null=True,
                                           default=0)
    experience_actual = models.IntegerField(verbose_name=_('Actual Experience'),
                                            null=True,
                                           default=0)
    level = models.ForeignKey(revengeLvl, verbose_name=_('Level'),
                              related_name='level_of_user',
                              null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class revengeMilestone(models.Model):
    milestone_date = models.DateTimeField(verbose_name=_("Milestone date"),
                              auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              related_name='owner_of_milestone',
                              blank=True)
    affected = models.ForeignKey(User, verbose_name=_('Affected'),
                              related_name='affected_of_milestone')

    comment = models.CharField(_('Comment'), max_length=250, blank=True)
    cat = models.ForeignKey(revengeCat, verbose_name=_('Category'))
    milestone = models.ForeignKey("self", verbose_name=_('Milestone contrattack'),
                          related_name=_('milestone_contrattack'),
                          null=True,
                          blank=True)

    def __str__(self):
        return u'De: %s Para: %s El %s' % (self.owner.username,
                              self.affected.username, self.milestone_date)


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
