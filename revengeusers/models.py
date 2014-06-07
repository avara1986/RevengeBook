# encoding: utf-8
import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, SiteProfileNotAvailable
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlquote

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


PROFILE_TYPES = (
        ('1', 'Público'),
        ('2', 'Amigos'),
    )
PROFILE_SEX = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
)


@python_2_unicode_compatible
class revengeUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=255, unique=True,
        help_text=_('Letters, numbers and @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    #TODO: unique=True,
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
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
    privacy = models.CharField(max_length=1, verbose_name=_('Privacidad'),
                                      choices=PROFILE_TYPES,
                                      default=1)
    sex = models.CharField(max_length=1, verbose_name=_('Sexo'),
                                      choices=PROFILE_SEX,
                                      default=1,
                                      blank=True)
    city = models.CharField(max_length=130, verbose_name=_('Ciudad'),
                                    blank=True)
    state = models.CharField(max_length=130, verbose_name=_('Provincia'),
                                    blank=True)
    country = models.CharField(max_length=130, verbose_name=_('País'),
                                    blank=True)
    url_twitter = models.CharField(max_length=130, verbose_name=_('URL Twitter'),
                                    blank=True)
    url_fb = models.CharField(max_length=130, verbose_name=_('URL FB'),
                                    blank=True)
    url_gpus = models.CharField(max_length=130, verbose_name=_('URL G Plus'),
                                    blank=True)
    url_revenge = models.CharField(max_length=130, verbose_name=_('URL RB'),
                                    blank=True)
    about_you = models.TextField(max_length=900, verbose_name=_('Acerca de ti'),
                                    blank=True)
    alert_revengers = models.TextField(max_length=900, verbose_name=_('Aviso a vengadores'),
                                    blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def is_friend_of(self, friend):
        try:
            friend = self.objects.get(friend=friend)
            return True
        except self.DoesNotExist:
            return False

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
