import string

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from pygments.lexer import default
from slugify import slugify

from .models import InstrumentCategory, Instrument

# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- ' + string.ascii_letters
#     code = 'letters+digits'
#
#     def __init__(self, message=None):
#         self.message = message if message else "В названии должны присутствовать только русские/английские символы, дефис и пробел"
#
#     def __call__(self, value, *args, **kwargs):
#         if set(value).issubset(self.ALLOWED_CHARS):
#             return
#         raise ValidationError(message=self.message, code=self.code)


# class AddInstrumentForm(forms.Form):
#     title = forms.CharField(max_length=255,
#                             min_length=5,
#                             label="Название прибора",
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#
#                             validators=[MinLengthValidator(5, message="Название слишком короткое"),
#                                         MaxLengthValidator(100),
#                                         ])
#     content = forms.CharField(widget=forms.Textarea, required=False, label="Описание")
#     is_published = forms.BooleanField(required=False, label="Статус", initial=True)
#     cat = forms.ModelChoiceField(queryset=InstrumentCategory.objects.all(),
#                                       label="Категория", empty_label="Категория не выбрана")
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- ' + string.ascii_letters
#         code = 'letters+digits'
#         message = "В названии должны присутствовать только русские/английские символы, дефис и пробел"
#
#         if set(title).issubset(ALLOWED_CHARS):
#             return
#         raise ValidationError(message=message, code=code)

class AddInstrumentForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=InstrumentCategory.objects.all(),
                                 label="Категория", empty_label="Категория не выбрана")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Instrument
        fields = ['title', 'content', 'is_published', 'cat', 'image', 'slug']
        widgets = { 'title' : forms.TextInput(attrs={'class': 'form-input'}),
                    'content' : forms.Textarea(attrs={'class': 'form-textarea'}),
                    }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- ' + string.ascii_letters
        code = 'letters+digits'
        message = "В названии должны присутствовать только русские/английские символы, дефис и пробел"

        if set(title).issubset(ALLOWED_CHARS):
            return title
        raise ValidationError(message=message, code=code)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="файл")