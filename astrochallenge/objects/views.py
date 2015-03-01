from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django_comments.views.utils import next_redirect
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.http import HttpResponse

from models import Constellation, CatalogObject, AstroObject, Observation
from astrochallenge.objects.forms import ObservationForm, FinderChartForm
from utils import FchartSettings, generate_fchart


@login_required
def delete_observation(request, observation_id):
    observation = get_object_or_404(Observation, pk=observation_id)
    redirect_url = observation.get_absolute_url()
    if not observation.user_profile == request.user.userprofile:
        return HttpResponseForbidden("You cannot delete this observation")
    else:
        observation.delete()
        return redirect(redirect_url)


@csrf_protect
@require_POST
def post_finderchart(request, next=None):
    data = request.POST.copy()
    content_type = data.get("content_type")
    object_id = data.get("object_id")
    if content_type is None or object_id is None:
        return ValueError("Missing content type or object id")
    model = ContentType.objects.get(pk=content_type).model_class()
    target = model.objects.get(pk=object_id)

    finder_chart_form = FinderChartForm(data)
    if not finder_chart_form.is_valid():
        messages.error(request, "Finder Chart form invalid")
        return next_redirect(request, fallback=next or target.get_absolute_url())
    settings = FchartSettings(
        limiting_magnitude_stars=finder_chart_form.cleaned_data['limiting_magnitude_stars'],
        limiting_magnitude_deepsky=finder_chart_form.cleaned_data['limiting_magnitude_deepsky'],
        fieldsize=finder_chart_form.cleaned_data['field_of_view']
    )

    settings.add_target(target.ra, target.dec, str(target), content_type, object_id)
    file = generate_fchart(settings)
    return HttpResponse("Posted" + file.name)


@csrf_protect
@login_required
@require_POST
def post_observation(request, next=None):
    data = request.POST.copy()
    content_type = data.get("content_type")
    object_id = data.get("object_id")
    if content_type is None or object_id is None:
        return ValueError("Missing content type or object id")
    model = ContentType.objects.get(pk=content_type).model_class()
    target = model.objects.get(pk=object_id)
    observation_form = ObservationForm(data)

    if not observation_form.is_valid():
        messages.error(request, "Observation form invalid")
        return next_redirect(request, fallback=next or observation_form.intsance.get_absolute_url())

    observation_form.instance.user_profile = request.user.userprofile

    if not target.observations.filter(user_profile__user__username=request.user.username).exists():
        try:
            observation_form.instance.points_earned = target.points
        except:
            pass

    observation_form.save()
    return next_redirect(request, fallback=next or observation_form.instance.get_absolute_url())


class SSODetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(SSODetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['current_info'] = self.get_object().observation_info(self.request.user.userprofile.observer)
            context['observation_form'] = ObservationForm(initial={
                'content_type': ContentType.objects.get(model="solarsystemobject").id,
                'object_id': self.get_object().pk,
                'lat': self.request.user.userprofile.lat,
                'lng': self.request.user.userprofile.lng,
                })
        return context


class DSODetailView(DetailView):
    def get_object(self):
        if self.kwargs.get('pk'):
            return get_object_or_404(AstroObject, pk=self.kwargs['pk'])
        catalog_object = get_object_or_404(CatalogObject, catalog=self.kwargs['catalog'], designation=self.kwargs['designation'])
        return catalog_object.astro_object

    def get_context_data(self, **kwargs):
        context = super(DSODetailView, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get(model="astroobject").id
        object_id = self.get_object().pk
        context['finder_chart_form'] = FinderChartForm(initial={
            'content_type': content_type,
            'object_id': object_id,
        })
        if self.request.user.is_authenticated():
            context['current_info'] = self.get_object().observation_info(self.request.user.userprofile.observer)
            context['observation_form'] = ObservationForm(initial={
                'content_type': content_type,
                'object_id': object_id,
                'lat': self.request.user.userprofile.lat,
                'lng': self.request.user.userprofile.lng,
            })
        return context


class DSOListView(TemplateView):
    template_name = "objects/astroobject_list.html"

    def get_context_data(self, **kwargs):
        context = super(DSOListView, self).get_context_data(**kwargs)
        context['constellations'] = [c.latin_name for c in Constellation.objects.all().order_by('latin_name')]
        if self.kwargs.get('catalog'):
            context['catalog'] = settings.CATALOGS[self.kwargs['catalog']]
            return context
        else:
            context['catalog'] = "All"
            return context


class DSOListViewJson(BaseDatatableView):
    model = AstroObject
    columns = ['pk', 'index', 'common_name', 'constellation.latin_name', 'type', 'magnitude', 'points', 'observed']
    order_columns = ['index', 'common_name', 'constellation.latin_name', 'type', 'magnitude', 'points', 'observed']

    def filter_queryset(self, qs):
        """ If search['value'] is provided then filter all searchable columns using istartswith
        """
        if not self.pre_camel_case_notation:
            # get global search value
            search = self.request.GET.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            for col_no, col in enumerate(col_data):
                # apply global search to all searchable columns
                if search and col['searchable']:
                    q |= Q(**{'{0}__icontains'.format(self.columns[col_no].replace(".", "__")): search})

                # column specific filter
                if col['search.value']:
                    qs = qs.filter(**{'{0}__icontains'.format(self.columns[col_no].replace(".", "__")): col['search.value']})
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        if column == "observed":
            if self.request.user.is_authenticated():
                if row.observations.filter(user_profile__user__username=self.request.user.username).exists():
                    return "<span class=\"green glyphicon glyphicon-ok\"></span>"
            return ""
        else:
            return super(DSOListViewJson, self).render_column(row, column)

    def get_initial_queryset(self):
        if not self.kwargs.get('catalog') or self.kwargs.get('catalog') == 'all':
            return AstroObject.objects.all()
        else:
            return AstroObject.objects.filter(catalogobject__catalog=self.kwargs['catalog'])
