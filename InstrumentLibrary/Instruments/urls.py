from django.urls import path, register_converter
from . import views, converters

from django.views.decorators.cache import cache_page

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.about, name='about'),
    path('instrument/<slug:instrument_slug>/', views.InstrumentView.as_view(), name='instrument'),
    path('category/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagView.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='update_page'),
]

