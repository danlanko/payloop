# Generated by Django 3.0.1 on 2020-01-15 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20200115_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='p_type',
            field=models.IntegerField(choices=[('1', 'All Package'), ('2', 'Custom'), ('3', 'Single Package')], default=1),
            preserve_default=False,
        ),
    ]
