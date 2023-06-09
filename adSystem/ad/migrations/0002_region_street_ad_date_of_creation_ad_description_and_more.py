# Generated by Django 4.2.1 on 2023-05-14 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя региона', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название улицы', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='date_of_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='description',
            field=models.CharField(default=1, help_text='Описание объявления', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.CharField(default=1, help_text='Назначенная цена', max_length=200),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Фио ползьователя', max_length=200)),
                ('avatar', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название города', max_length=100)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ad.region')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ad.city'),
        ),
        migrations.AddField(
            model_name='ad',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ad.street'),
        ),
    ]
