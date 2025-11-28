from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.index, name='home'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('instrument/<int:instrument_id>/', views.show_instrument, name='instrument'),
    path('category/<int:category_id>/', views.show_category, name='category'),
]

