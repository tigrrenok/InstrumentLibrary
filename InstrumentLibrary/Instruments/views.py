from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.template.defaultfilters import title
from django.urls import reverse

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Ионный хроматограф ICS-6000', 'content': '''Dionex ICS-6000 – это многофункциональная система для ионной хроматографии (ИХ), которая разработана для выполнения комплексного анализа. В зависимости от конфигурации прибора на нем можно решать как рутинные лабораторные задачи по контролю качества, так и выполнять самые передовые исследования, а также проводить анализ следовых количеств компонентов. Больше нет ограничений при выборе методики, ионный хроматограф ICS-6000 позволяет запустить любое приложение для ИХ. Вы можете заниматься разработкой, исследованиями, рутинными задачами, и при этом запускать различные методы одновременно на одном приборе.''', 'is_published': True},
    {'id': 2, 'title': 'Ионный хроматограф Aquion', 'content': '''Простой, с инженерной точки зрения, ионный хроматограф Dionex Aquion позволяет получать надежные результаты анализов и катионов, и анионов.''', 'is_published': True},
    {'id': 3, 'title': 'Ионный хроматограф Integrion', 'content': '''Ионный хроматограф (ИХ) Dionex Integrion позволяет автоматизировать большую часть аналитических процедур. Достаточно просто подключить источник с деионизированной водой к прибору, а все остальное ИХ Integrion сделает сам: система сгенерирует нужный элюент, позаботится о подавлении противоионов. Гибкая платформа настраивается под различные применения, например, для анализа загрязнений окружающей среды, сахаров и простых углеводов в продуктах питания и напитках, ионных соединений в фармацевтических препаратах, а также востребована в промышленных и нефтехимических приложениях. Немаловажно, что по мере возникновения в лаборатории новых потребностей, система может быть модифицирована и адаптирована под другие методики.''', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Титраторы'},
    {'id': 2, 'name': 'Ионные хроматографы'},
    {'id': 3, 'name': 'рН-метры'},
]

# Create your views here.
def index(request):
    data = {'title': "Главная страница",
            'menu': menu,
            'instruments': data_db,
            'cat_selected': 0}
    return render (request, 'Instruments/index.html', context=data)

def about(request):
    data = {'title': "О компании",
            'menu': menu}
    return render(request, 'Instruments/about.html', context=data)


def show_instrument(request, instrument_id):
    data = {'title': f"О приборе c id: {instrument_id}",
            'menu': menu}
    return HttpResponse(f"О приборе c id: {instrument_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")


def addpage(request):
    return HttpResponse("Добавить статью")


def contact(request):
    return HttpResponse("Контакты")


def login(request):
    return HttpResponse("Войти")


def show_category(request, category_id):
    data = {'title': "Главная страница",
            'menu': menu,
            'instruments': data_db,
            'cat_selected': category_id}
    return render (request, 'Instruments/index.html', context=data)