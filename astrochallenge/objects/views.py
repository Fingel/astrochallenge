from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings

from models import Constellation, CatalogObject, AstroObject


class DSODetailView(DetailView):
    def get_object(self):
        if self.kwargs.get('pk'):
            return get_object_or_404(AstroObject, pk=self.kwargs['pk'])
        catalog_object = get_object_or_404(CatalogObject, catalog=self.kwargs['catalog'], designation=self.kwargs['designation'])
        return catalog_object.astro_object


class DSOListView(ListView):
    def get_queryset(self):
        if self.kwargs.get('catalog'):
            return AstroObject.objects.filter(catalogobject__catalog=self.kwargs['catalog'])
        else:
            return AstroObject.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DSOListView, self).get_context_data(**kwargs)
        context['constellations'] = [c.latin_name for c in Constellation.objects.all().order_by('latin_name')]
        if self.kwargs.get('catalog'):
            context['catalog'] = settings.CATALOGS[self.kwargs['catalog']]
            return context
        else:
            context['catalog'] = "All"
            return context
