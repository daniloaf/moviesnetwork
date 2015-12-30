from django.conf.urls import url

from views import SearchActorView

SEARCH_ACTOR = 'search_actor'

urlpatterns = [
    url(r'search/actor', SearchActorView.as_view(), name=SEARCH_ACTOR)
]
