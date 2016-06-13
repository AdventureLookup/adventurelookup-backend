import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from . import models


class AdventureById(View):
    def dispatch(self, request, *args, **kwargs):
        self.adventure_id = kwargs.get('adventure_id')
        return super().dispatch(request)

    def get(self, request):
        adventure = get_object_or_404(models.Adventure, pk=self.adventure_id)
        data = model_to_dict(adventure)
        return JsonResponse(data)

    def put(self, request):
        new_data = json.loads(request.body.decode('utf-8'))

        adventure_qset = models.Adventure.objects.filter(pk=self.adventure_id)
        if not adventure_qset:
            return JsonResponse({}, status=404,
                                reason='No Adventure matches the given query.')
        adventure_qset.update(**new_data)
        adventure_data = model_to_dict(adventure_qset[0])
        return JsonResponse(adventure_data)
