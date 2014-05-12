from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    friends = models.ManyToManyField("self", verbose_name=_('Friends'),
                                    related_name='friends',
                                    null=True,
                                    blank=True)
    avatar = models.ImageField(upload_to="avatars")

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class revengePointCat(models.Model):
    title = models.CharField(_('title'), max_length=230, unique=True)
    image = models.ImageField(upload_to="revengePointsCats", blank=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class revengePoint(models.Model):
    title = models.CharField(_('title'), max_length=230, unique=True)
    description = models.CharField(_('description'), max_length=550, blank=True)
    image = models.ImageField(upload_to="revengePoints", blank=True)
    cat = models.ForeignKey(revengePointCat, verbose_name=_('Category'))

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class revengeMilestone(models.Model):
    title = models.CharField(verbose_name=_('title'),
                            blank=True,
                            max_length=230)
    milestone_date = models.DateTimeField(verbose_name=_("Milestone date"),
                              auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              related_name='owner_of_milestone',
                              blank=True)
    affected = models.ForeignKey(User, verbose_name=_('Affected'),
                              related_name='affected_of_milestone')

    comment = models.CharField(_('Comment'), max_length=250, blank=True)
    point = models.ForeignKey(revengePoint, verbose_name=_('Point'))

    def __str__(self):
        return u'De: %s Para: %s El %s' % (self.owner.username,
                              self.affected.username, self.milestone_date)
