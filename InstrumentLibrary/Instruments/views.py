from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.defaultfilters import title
from django.urls import reverse

import Instruments
from .models import Instrument, InstrumentCategory, TagInstrument

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


# Create your views here.
def index(request):
    instruments = Instrument.published_objects.all()
    data = {'title': "Главная страница",
            'menu': menu,
            'instruments': instruments,
            'cat_selected': 0}
    return render (request, 'Instruments/index.html', context=data)

def about(request):
    data = {'title': "О компании",
            'menu': menu}
    return render(request, 'Instruments/about.html', context=data)


def show_instrument(request, instrument_slug):
    instrument = get_object_or_404(Instrument, slug=instrument_slug)
    data = {
        'title': instrument.title,
        'menu': menu,
        'instrument': instrument,
        'cat_selected': 1
    }

    return render(request, 'Instruments/instrument.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")


def addpage(request):
    return HttpResponse("Добавить статью")


def contact(request):
    return HttpResponse("Контакты")


def login(request):
    return HttpResponse("Войти")


def show_category(request, category_slug):
    category = get_object_or_404(InstrumentCategory, slug=category_slug)
    instruments = Instrument.published_objects.filter(cat_id=category.pk)

    data = {'title': f"Приборы в категории {category.name}",
            'menu': menu,
            'instruments': instruments,
            'cat_selected': category.pk}
    return render (request, 'Instruments/index.html', context=data)


def show_tag(request, tag_slug):
    tag = get_object_or_404(TagInstrument, slug=tag_slug)
    instruments = tag.instruments.filter(is_published=Instrument.Status.PUBLISHED)

    data = {'title': f"Приборы в категории {tag.name}",
            'menu': menu,
            'instruments': instruments,
            'cat_selected': None}
    return render(request, 'Instruments/index.html', context=data)