from django.db import models
from django.urls import reverse
import os

import datetime


def get_image_filename(instance, filename):
    """Функция для генерации уникального имени файла изображения с датой"""
    ext = filename.split('.')[-1]  # определяем расширение файла изображения
    now = datetime.datetime.now()  # получаем текущую дату и время
    filename = f'{now.strftime("%Y-%m-%d %H:%M:%S")}.{ext}'  # создаем уникальное имя файла с датой и расширением
    return os.path.join('images/', filename)  # возвращаем имя файла


class Ad(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, help_text='Название объявления')
    description = models.TextField(max_length=500, help_text='Описание объявления')
    price = models.CharField(max_length=200, help_text='Назначенная цена')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, blank=True, null=True)
    street = models.ForeignKey('Street', on_delete=models.SET_NULL, blank=True, null=True)
    house = models.CharField(max_length=200, help_text='Номер дома', blank=True, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('Individual', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.DO_NOTHING)
    img = models.ImageField(upload_to=get_image_filename, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('ad-detail', args=[str(self.id)])

    def __str__(self):
        return self.name;


class Type(models.Model):
    name = models.CharField(max_length=100, help_text='Название типа')

    def __str__(self):
        return self.name;


class Region(models.Model):
    name = models.CharField(max_length=100, help_text='Имя региона')

    def __str__(self):
        return self.name;


class City(models.Model):
    name = models.CharField(max_length=100, help_text='Название города')
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name;

class Offer(models.Model):
    customer = models.ForeignKey('Individual', on_delete=models.CASCADE)
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    new_price = models.IntegerField(blank=True, null=True, help_text='Предложение новой цены')
    description = models.TextField(max_length=200, blank=True, null=True, help_text='Описание предложения')



class Street(models.Model):
    name = models.CharField(max_length=100, help_text='Название улицы')

    def __str__(self):
        return self.name;


class Individual(models.Model):
    name = models.CharField(max_length=200, help_text="Фио ползьователя")
    avatar = models.ImageField(blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=50, help_text="Номер телефона")

    def get_absolute_url(self):
        return reverse('individual-detail', args=[str(self.id)])

    def __str__(self):
        return self.name;
