from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'revengeBook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile/', RedirectView.as_view(url='/revenge-panel/', permanent=False), name='redirect_revenge_panel'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('revengeapp.urls')),
    url(r'^', include('milestones.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
