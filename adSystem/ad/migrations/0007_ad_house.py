# Generated by Django 4.2.1 on 2023-05-15 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0006_ad_owner_alter_individual_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='house',
            field=models.CharField(blank=True, help_text='Номер дома', max_length=200, null=True),
        ),
    ]
