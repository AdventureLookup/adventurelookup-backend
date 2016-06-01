from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adventure/(.+)$', views.:adventure_by_id),
]