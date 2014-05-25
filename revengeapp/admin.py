from django.contrib import admin
from revengeapp.models import revengeExpType, revengeExpLog


class revengeExpTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'points')


admin.site.register(revengeExpType, revengeExpTypeAdmin)
admin.site.register(revengeExpLog)
