from django import forms
from .models import Product


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, label='Электронная почта:')
    name = forms.CharField(required=True, label='Имя:')
    surname = forms.CharField(required=True, label='Фамилия:')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class LoginForm(forms.Form):
    name = forms.CharField(required=True, label='Имя:')
    surname = forms.CharField(required=True, label='Фамилия:')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


def get_products():
    products = Product.objects.all()
    choices = []
    for each in products:
        choices.append((each.name, each.name))
    return choices


class PublicationForm(forms.Form):
    title = forms.CharField(max_length=20, label='Тема')
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Проблема', 'Проблема'),
                                                                    ('Предложение', 'Предложение')],
                                 label='Категория')
    desc = forms.CharField(widget=forms.Textarea, label='Описание')
    product = forms.ChoiceField(choices=get_products(), label='Товар')


class CommentForm(forms.Form):
    desc = forms.CharField(widget=forms.Textarea, label='Введите комментарий')
    required_css_class = 'commentForm'


class RegistrationStaffForm(forms.Form):
    email = forms.EmailField(required=True, label='Электронная почта:')
    name = forms.CharField(required=True, label='Имя:')
    surname = forms.CharField(required=True, label='Фамилия:')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=[('Модератор', 'Модератор'),
                                      ('Поддержка', 'Поддержка'),
                                      ('Аналитик', 'Аналитик')], label='Роль')

# def insert_products():
#     Product.objects.create(name='BMW X5', price=9900000)
#     Product.objects.create(name='BMW i7', price=7500000)
#     Product.objects.create(name='BMW M3', price=11000000)
