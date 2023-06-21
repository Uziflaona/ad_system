from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Individual, Ad, Type, City, Street, Offer
from django.forms import ValidationError
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=12)

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        name = self.cleaned_data.get('name')

        if commit:
            user.save()

            individual = Individual(name=name, user=user)
            individual.save()
            # сохраняем профиль второй модели

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'phone_number')

class CreateAdForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите имя...'}), required=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Введите описание объявления...'}), required=False)
    price = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите цену...'}), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    street = forms.ModelChoiceField(queryset=Street.objects.all(), required=False)
    house = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите номер дома'}), required=False)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True)
    image = forms.ImageField(required=False)


    class Meta:
        model = Ad
        fields = ['name', 'description', 'price', 'city', 'street', 'house', 'type', 'image']

class EditAdForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите имя...'}),
                           required=True)
    description = forms.CharField(max_length=500,
                                  widget=forms.Textarea(attrs={'placeholder': 'Введите описание объявления...'}),
                                  required=False)
    price = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите цену...'}),
                            required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    street = forms.ModelChoiceField(queryset=Street.objects.all(), required=False)
    house = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Введите номер дома'}),
                            required=False)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Ad
        fields = ['name', 'description', 'price', 'city', 'street', 'house', 'type', 'image']


class IndividualForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=30, help_text="Логин пользователя",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, max_length=254, help_text="Email пользователя",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, max_length=128, help_text="Пароль пользователя",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, max_length=200, help_text="ФИО пользователя",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, help_text="Фотография пользователя")
    phone_number = forms.CharField(required=True, max_length=50, help_text="Номер телефона",
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Individual
        fields = ('name', 'avatar', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавление элементов для редактирования пользователя
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

        self.fields['password'].required = False

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.user_id).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.user_id).exists():
            raise ValidationError("Email address already exists")
        return email

    def save(self, commit=True):
        individual = super().save(commit=False)
        if commit:
            user = individual.user if individual.user else User()
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            individual.user = user
            individual.save()
        return individual

class OfferCreate(forms.ModelForm):


    class Meta:
        model = Offer
        fields = ('new_price', 'description')
        labels = ('Цена', 'Описание')
