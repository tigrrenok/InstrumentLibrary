from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import UploadFileForm
from .mixins import DataMixin
from .models import Instrument, UploadedFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class Home(DataMixin, ListView):
    model = Instrument
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Instrument.published_objects.all().select_related('cat')

@login_required
def about(request):
    contact_list = Instrument.published_objects.all().select_related('cat')
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'Instruments/about.html',
                  context={'title': "О сайте", 'page_obj': page_obj})



class InstrumentView(DataMixin, DetailView):
    template_name = 'Instruments/instrument.html'
    slug_url_kwarg = 'instrument_slug'
    context_object_name = 'instrument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['instrument'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Instrument.published_objects, slug=self.kwargs[self.slug_url_kwarg])



def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")



class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    model = Instrument
    fields = '__all__'
    template_name = 'Instruments/addpage.html'
    title_page = 'Добавление прибора'
    permission_required = 'Instrument.add_instrument'


class UpdatePage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Instrument
    fields = '__all__'
    template_name = 'Instruments/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирвание прибора'
    permission_required = 'Instrument.change_instrument'


def contact(request):
    return HttpResponse("Контакты")


def login(request):
    return HttpResponse("Войти")


class CategoryView(DataMixin, ListView):
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    allow_empty = False

    def get_queryset(self):
        instruments = Instrument.published_objects.filter(cat__slug=self.kwargs['category_slug']).select_related('cat')
        return instruments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['instruments'][0].cat
        return self.get_mixin_context(context, title=f"Категрия - {cat.name}", cat_selected=cat.pk)


class TagView(DataMixin, ListView):
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    allow_empty = False

    def get_queryset(self):
        instruments = Instrument.published_objects.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
        return instruments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['instruments'][0].cat
        return self.get_mixin_context(context, title=f"Приборы в категории {tag.name}")
