
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, ModelForm, RadioSelect
from .models import Save_user_data, Product



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Ім’я користувача",
        widget=forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Ім’я користувача'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'my_st_number', 'placeholder': 'Введіть пароль'})
    )


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'my_st_number', 'placeholder': 'Введіть пароль'}),
        help_text=""
    )

    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={'class': 'my_st_number', 'placeholder': 'Підтвердіть пароль'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Ім’я користувача'}),
        }

class Save_user_data_form(forms.ModelForm):
    class Meta:
        model = Save_user_data
        fields = ("name", "phone", "email", "address_nova_poshta", "city_nova_poshta", "region_nova_poshta", "branch_nova_poshta", "address_ukr_poshta", "city_ukr_poshta", "region_ukr_poshta", "inbex_ukr_poshta")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Ім’я' , 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Телефон' , 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'my_st_number', 'placeholder': 'Email'}),
            'address_nova_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Адреса'}),
            'city_nova_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Місто'}),
            'region_nova_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Область'}),
            'branch_nova_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Відділення'}),
            'address_ukr_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Адреса'}),
            'city_ukr_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Місто'}),
            'region_ukr_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Область'}),
            'inbex_ukr_poshta': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Індекс'}),
        }

class Product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "image",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "image_5",
            "name",
            "description",
            "price",
            "for_dad",
            "for_mom",
            "is_available"
        )
        widgets = {
            'category': forms.Select(attrs={'class': 'my_st_number', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'image_1': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'image_4': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'image_5': forms.ClearableFileInput(attrs={'class': 'my_st_number'}),
            'name': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Ім’я', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'my_st_number', 'placeholder': 'Опис'}),
            'price': forms.TextInput(attrs={'class': 'my_st_number', 'placeholder': 'Ціна'}),
            'for_dad': forms.CheckboxInput(attrs={'class': 'my_st_number'}),
            'for_mom': forms.CheckboxInput(attrs={'class': 'my_st_number'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'my_st_number'}),
        }