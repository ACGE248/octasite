# Generated by Django 3.2.16 on 2023-01-28 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('octapply', '0004_auto_20230128_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='degree_lvl',
        ),
    ]