from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
#from revengeapp.models import revengeExpLog, revengeExpType


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


    def get_exp_total(self):
        experience = self.experience_total
        return self.check_exp_no_blank(experience)

    def get_exp_actual(self):
        experience = self.experience_actual
        return self.check_exp_no_blank(experience)

    def check_exp_no_blank(self, experience):
        if isinstance(experience, int) and experience != "":
            return experience
        else:
            return 0

    def add_exp(self, typeExpTag):
        from revengeapp.models import revengeExpType
        try:
            exp_type = revengeExpType.objects.get(tag=typeExpTag)
        except self.DoesNotExist:
            return False
        # Add total exp
        self.add_exp_total(exp_type.points)
        # Add Actual exp and update level if proceded
        self.add_exp_actual(exp_type.points)
        self.log_exp(exp_type)

    def add_exp_total(self, points):
        experience_total = self.get_exp_total()
        self.experience_total = experience_total + points
        self.save()

    def add_exp_actual(self, points):
        experience_actual = self.get_exp_actual()
        levelActual = revengeLvl.objects.get(id=self.level.id)
        if levelActual.points <= (experience_actual + points):
            expNexLevel = (experience_actual + points) - levelActual.points
            self.experience_actual = expNexLevel
            self.level = revengeLvl.objects.get(id=(self.level.id + 1))
            self.save()
        else:
            self.experience_actual = experience_actual + points
            self.save()

    def log_exp(self, exp_type, *arg, **kwarg):
        from revengeapp.models import revengeExpLog
        log = revengeExpLog.objects.create(owner=self, type=exp_type)
        log.save()

    def __str__(self):
        return self.username
