# Generated by Django 3.2.16 on 2023-02-02 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octapply', '0008_program_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='university',
            field=models.ManyToManyField(related_name='university', to='octapply.University'),
        ),
    ]