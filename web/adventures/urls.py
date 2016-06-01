from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adventure/(.+)$', views.get_adventure_by_id),
]