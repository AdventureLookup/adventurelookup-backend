from django.conf.urls import url

from . import views

urlpatterns = [url(r'^adventure/(?P<adventure_id>\d+)$', views.AdventureById.as_view(), name="adventure-by-id"), ]
