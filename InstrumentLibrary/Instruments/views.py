from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import request
from django.template.defaultfilters import title
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from slugify import slugify

from . import forms
from .forms import UploadFileForm, AddInstrumentForm
from .models import Instrument, InstrumentCategory, TagInstrument, UploadedFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]



class Home(ListView):
    model = Instrument
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    extra_context = {
        'title': "Главная страница",
        'menu': menu,
        'cat_selected': 0}

    def get_queryset(self):
        return Instrument.published_objects.all().select_related('cat')


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadedFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    data = {
        'title': "О компании",
            'menu': menu,
            'form': form,
            }
    return render(request, 'Instruments/about.html', context=data)


class InstrumentView(DetailView):
    # model = Instrument
    template_name = 'Instruments/instrument.html'
    slug_url_kwarg = 'instrument_slug'
    context_object_name = 'instrument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['instrument'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Instrument.published_objects, slug=self.kwargs[self.slug_url_kwarg])



def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")


# class AddPage(View):
#     def get(self, request):
#         form = forms.AddInstrumentForm()
#         data = {
#             'title': "Добавление статьи",
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'Instruments/addpage.html', context=data)
#
#     def post(self, request):
#         form = forms.AddInstrumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             slug = slugify(title)
#
#             try:
#                 Instrument.objects.create(**form.cleaned_data, slug=slug)
#                 return redirect(reverse('instrument', kwargs={'instrument_slug': slug}))
#             except IntegrityError:
#                 form.add_error(None, "Такой прибор уже существует")
#             except:
#                 form.add_error(None, "Ошибка добавления поста")
#             data = {
#                 'title': "Добавление статьи",
#                 'menu': menu,
#                 'form': form,
#             }
#             return render(request, 'Instruments/addpage.html', context=data)

class AddPage(CreateView):
    model = Instrument
    fields = '__all__'
    template_name = 'Instruments/addpage.html'
    # success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление прибора'
        context['menu'] = menu
        return context

class UpdatePage(UpdateView):
    model = Instrument
    fields = '__all__'
    template_name = 'Instruments/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирвание прибора'
        context['menu'] = menu
        return context

def contact(request):
    return HttpResponse("Контакты")


def login(request):
    return HttpResponse("Войти")


class CategoryView(ListView):
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    allow_empty = False

    def get_queryset(self):
        instruments = Instrument.published_objects.filter(cat__slug=self.kwargs['category_slug']).select_related('cat')
        return instruments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['instruments'][0].cat
        context['title'] = f"Категрия - {cat.name}"
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


class TagView(ListView):
    template_name = 'Instruments/index.html'
    context_object_name = 'instruments'
    allow_empty = False

    def get_queryset(self):
        instruments = Instrument.published_objects.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
        return instruments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['instruments'][0].cat
        context['title'] = f"Приборы в категории {tag.name}"
        context['menu'] = menu
        context['cat_selected'] = None
        return context




# def show_tag(request, tag_slug):
#     tag = get_object_or_404(TagInstrument, slug=tag_slug)
#     instruments = tag.instruments.filter(is_published=Instrument.Status.PUBLISHED).select_related('cat')
#
#     data = {'title': f"Приборы в категории {tag.name}",
#             'menu': menu,
#             'instruments': instruments,
#             'cat_selected': None}
#     return render(request, 'Instruments/index.html', context=data)


# def show_category(request, category_slug):
#     category = get_object_or_404(InstrumentCategory, slug=category_slug)
#     instruments = Instrument.published_objects.filter(cat_id=category.pk).select_related('cat')
#
#     data = {'title': f"Приборы в категории {category.name}",
#             'menu': menu,
#             'instruments': instruments,
#             'cat_selected': category.pk}
#     return render (request, 'Instruments/index.html', context=data)

# def addpage(request):
#     if request.method == 'POST':
#         form = forms.AddInstrumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             slug = slugify(title)
#
#             try:
#                 Instrument.objects.create(**form.cleaned_data, slug=slug)
#                 return redirect(reverse('instrument', kwargs={'instrument_slug': slug}))
#             except IntegrityError:
#                 form.add_error(None, "Такой прибор уже существует")
#             except:
#                 form.add_error(None, "Ошибка добавления поста")
#     else:
#         form = forms.AddInstrumentForm()
#     data = {
#             'title': "Добавление статьи",
#             'menu': menu,
#             'form': form,
#     }
#     return render(request, 'Instruments/addpage.html', context=data)

# def index(request):
#     instruments = Instrument.published_objects.all().select_related('cat')
#     data = {'title': "Главная страница",
#             'menu': menu,
#             'instruments': instruments,
#             'cat_selected': 0}
#     return render (request, 'Instruments/index.html', context=data)


# def show_instrument(request, instrument_slug):
#     instrument = get_object_or_404(Instrument, slug=instrument_slug)
#     data = {
#         'title': instrument.title,
#         'menu': menu,
#         'instrument': instrument,
#         'cat_selected': 1
#     }
#
#     return render(request, 'Instruments/instrument.html', context=data)