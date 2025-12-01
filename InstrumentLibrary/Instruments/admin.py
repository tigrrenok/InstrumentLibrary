from django.contrib import admin, messages

from .models import Instrument, InstrumentCategory
# Register your models here.

class SpecificationFilter(admin.SimpleListFilter):
    title = "Наличие спецификации"
    parameter_name = "specification"

    def lookups(self, request, model_admin):
        return [
            ('has-spec', 'есть спецификация'),
            ('no-spec', 'нет спецификации')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'has-spec':
            return queryset.filter(specifications__isnull=False)
        return queryset.filter(specifications__isnull=True)

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'brief_info', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ('title', )
    search_fields = ('title', 'content', 'cat__name')
    # list_editable = ('is_published',)
    list_per_page = 20
    actions = ['set_obsolete', 'set_actual']
    list_filter = (SpecificationFilter, 'is_published', 'cat__name')
    readonly_fields = ('slug', )

    @admin.display(description='Краткое описание')
    def brief_info(self, instrument):
        return instrument.content[:45]

    @admin.action(description="Пометить снятыми с производства")
    def set_obsolete(self, request, queryset):
        count = queryset.update(is_published=0)
        self.message_user(request, f'{count} записей убрано из актуального оборудования', messages.WARNING)

    @admin.action(description="Пометить доступными к приобретению")
    def set_actual(self, request, queryset):
        count = queryset.update(is_published=1)
        self.message_user(request, f'Изменено {count} записей')


@admin.register(InstrumentCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_display_links = ('name', 'id')
    ordering = ('name', )
    search_fields = ('name', )



