from django.conf.urls import patterns, include, url
from milestones.views import MilestoneListView

ajax_urlpatterns = patterns('milestones.ajax',
    url(r'^add-milestone/$', 'add_milestone', name='add_milestone_ajax'),
)
views_urlpatterns = patterns('milestones.views',
    url(r'^milestones/(?P<idfriend>[0-9]{0,15})/$', MilestoneListView.as_view(), name='milestones'),
    url(r'^milestone_form/$', 'milestones_form', name='milestones_form'),
)
urlpatterns = patterns('',
    url(r'^', include(views_urlpatterns)),
    url(r'^kwsn/', include(ajax_urlpatterns)),
)
