from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from . import models


def adventure_by_id(request, adventure_id):
    # This endpoint only handles information retrieval, so only GET
    # requests are allowed. Respond with 'METHOD NOT ALLOWED'.
    if request.method != 'GET':
        return HttpResponse(status=405)

    adventure = get_object_or_404(models.Adventure, pk=adventure_id)
    data = model_to_dict(adventure)
    return JsonResponse(data)
