from django.conf.urls import patterns, include, url

ajax_urlpatterns = patterns('revengeapp.ajax',
    url(r'^search-friends/$', 'search_friend', name='search_friend'),
    url(r'^search-my-friend/$', 'search_my_friend', name='search_my_friend'),
    url(r'^add-milestone/$', 'add_milestone', name='add_milestone'),
)
views_urlpatterns = patterns('revengeapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^sign-up/$', 'sign_up', name='sign_up'),
    url(r'^revenge-panel/', 'revenge_panel', name='RevengePanel'),
    url(r'^sign-out/$', 'sign_out', name='sign_out'),
    url(r'^search-friend/$', 'search_friend', name='searchFriend'),
    url(r'^profile/(?P<idfriend>[0-9]{0,15})/$', 'see_profile', name='see_profile'),
    url(r'^kwsn/', include(ajax_urlpatterns)),
)
urlpatterns = patterns('',
    url(r'^', include(views_urlpatterns)),
    url(r'^kwsn/', include(ajax_urlpatterns)),
)
