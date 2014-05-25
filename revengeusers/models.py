from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

#from revengeapp.models import revengeLvl


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
