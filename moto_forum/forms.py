from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['brand'].empty_label = 'Марка не выбрана'

    class Meta:
        model = Motorcycle
        fields = ['brand', 'category', 'model', 'slug', 'content', 'photo', 'is_published']  # '__all__'
        widgets = {
            'model': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_model(self):
        model = self.cleaned_data['model']
        if len(model) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return model


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Введите символы с картинки')
