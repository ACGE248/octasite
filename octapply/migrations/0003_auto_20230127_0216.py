# Generated by Django 3.2.16 on 2023-01-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octapply', '0002_auto_20230127_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='fall_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='spring_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='summer_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='winter_deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
