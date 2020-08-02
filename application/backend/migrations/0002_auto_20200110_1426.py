# Generated by Django 3.0.1 on 2020-01-10 13:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='company_name',
            field=models.CharField(default='sdasd', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='email',
            field=models.EmailField(default='da@da.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='expiry_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]