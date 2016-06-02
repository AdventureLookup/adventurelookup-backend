from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.generic import View
from . import models


class AdventureById(View):

    def dispatch(self, request, *args, **kwargs):
        self.adventure_id = kwargs.get('adventure_id')
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        adventure = get_object_or_404(models.Adventure, pk=self.adventure_id)
        data = model_to_dict(adventure)
        return JsonResponse(data)
