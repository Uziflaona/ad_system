from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Individual, Ad, Type, City, Street
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=255)

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
        fields = ('username', 'email', 'password1', 'password2', 'name')

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
