from django.core.exceptions import ObjectDoesNotExist

from revengeapp.models import User, revengeExpLog, revengeExpType
from revengeusers.models import revengeLvl


class revengeUser(object):
    model = ""

    def __init__(self, user):
        self.set_user(user)

    def set_user(self, user):
        self.model = user

    def get_user(self):
        return self.model

    def check_userModel(self):
        return isinstance(self.model, User)

    def get_exp_total(self):
        if self.check_userModel():
            experience = self.model.experience_total
            return self.check_exp_no_blank(experience)
        else:
            return False

    def get_exp_actual(self):
        if self.check_userModel():
            experience = self.model.experience_actual
            return self.check_exp_no_blank(experience)
        else:
            return False

    def check_exp_no_blank(self, experience):
        if isinstance(experience, int) and experience != "":
            return experience
        else:
            return 0

    def add_exp(self, typeExpTag):
        if self.check_userModel():
            try:
                exp_type = revengeExpType.objects.get(tag=typeExpTag)
            except ObjectDoesNotExist:
                return False
            # Add total exp
            self.add_exp_total(exp_type.points)
            # Add Actual exp and update level if proceded
            self.add_exp_actual(exp_type.points)
            self.log_exp(exp_type)
        else:
            return False

    def add_exp_total(self, points):
        experience_total = self.get_exp_total()
        self.model.experience_total = experience_total + points
        self.model.save()

    def add_exp_actual(self, points):
        experience_actual = self.get_exp_actual()
        levelActual = revengeLvl.objects.get(id=self.model.level.id)
        if levelActual.points <= (experience_actual + points):
            expNexLevel = (experience_actual + points) - levelActual.points
            self.model.experience_actual = expNexLevel
            self.model.level = revengeLvl.objects.get(id=(self.model.level.id + 1))
            self.model.save()
        else:
            self.model.experience_actual = experience_actual + points
            self.model.save()

    def log_exp(self, exp_type, *arg, **kwarg):
        if self.check_userModel():
            log = revengeExpLog.objects.create(owner=self.model, type=exp_type)
            log.save()
        else:
            return False
