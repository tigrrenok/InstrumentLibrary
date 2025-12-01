from django import template

from Instruments.models import InstrumentCategory, TagInstrument

register = template.Library()

@register.inclusion_tag('Instruments/list_categories.html')
def show_categories(cat_selected=0):
    cats = InstrumentCategory.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('Instruments/list_tags.html')
def show_all_tags():
    return {'tags': TagInstrument.objects.all()}