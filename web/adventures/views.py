from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from . import models


def adventure_by_id(request, adventure_id):
    # This endpoint only handles information retrieval, so only GET
    # requests are allowed. Respond with 'METHOD NOT ALLOWED'.
    if request.method != 'GET':
        return HttpResponse(status=405)

    # Adventure IDs must be integers, respond with BAD REQUEST if an
    # invalid ID is given.
    is_valid_id = all(char.isdigit() for char in adventure_id)
    if not is_valid_id:
        return HttpResponse(status=400, reason='Invalid adventure ID.')

    adventure = get_object_or_404(models.Adventure, pk=adventure_id)
    data = model_to_dict(adventure)
    return JsonResponse(data)
