from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from . import models


class AdventureById(View):
    def dispatch(self, request, *args, **kwargs):
        adventure_id = kwargs.get('adventure_id')
        self.adventure = get_object_or_404(models.Adventure, pk=adventure_id)
        return super().dispatch(request)

    def get(self, request):
        data = model_to_dict(self.adventure)
        return JsonResponse(data)
