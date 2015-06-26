from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from astrochallenge.objects.models import Supernova
from astrochallenge.objects.plots import supernova_light_curve


def snlightcurve(request, supernova_id):
    sn = get_object_or_404(Supernova, pk=supernova_id)
    plt = supernova_light_curve(sn)
    response = HttpResponse(content_type='image/png')
    plt.savefig(response)
    plt.close()
    return response
