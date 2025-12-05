import string

from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from pygments.lexer import default
from slugify import slugify

from .models import InstrumentCategory, Instrument


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

class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.username
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True
        else:
            self.fields['captcha'] = CaptchaField(label="Введите указанные символы")