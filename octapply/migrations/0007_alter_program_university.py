# Generated by Django 3.2.16 on 2023-01-29 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octapply', '0006_program_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='university',
            field=models.ManyToManyField(related_name='uni', to='octapply.University'),
        ),
    ]