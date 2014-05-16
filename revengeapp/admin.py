from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from revengeapp.models import revengeMilestone, revengeCat, revengeLvl, revengeExpType, revengeExpLog
from revengeapp.forms import RevengeUserCreationForm, RevengeUserChangeForm


class RevengeUserAdmin(UserAdmin):
    add_form = RevengeUserCreationForm
    form = RevengeUserChangeForm
    filter_horizontal = UserAdmin.filter_horizontal + ('friends',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Revenge data'), {'fields': ('friends','avatar')}),
        (_('Revenge experience'), {'fields': ('experience_total','experience_actual','level')}),
    )


class revengeLvlAdmin(admin.ModelAdmin):
    list_display = ('title', 'points',)


class revengeExpTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'points')

admin.site.register(get_user_model(), RevengeUserAdmin)
admin.site.register(revengeMilestone)
admin.site.register(revengeCat)
admin.site.register(revengeLvl, revengeLvlAdmin)
admin.site.register(revengeExpType, revengeExpTypeAdmin)
admin.site.register(revengeExpLog)
