from django.conf.urls import url

from views import SearchActorView, ActorView

SEARCH_ACTOR = 'search_actor'
ACTOR = 'actor'

urlpatterns = [
    url(r'search/actor/?', SearchActorView.as_view(), name=SEARCH_ACTOR),
    url(r'actor/(?P<actor_id>\d+)/?', ActorView.as_view(), name=ACTOR)
]
