# Generated by Django 3.2.16 on 2023-01-28 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octapply', '0005_remove_program_degree_lvl'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='university',
            field=models.ManyToManyField(to='octapply.University'),
        ),
    ]