# Generated by Django 4.2.7 on 2023-11-23 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathfinder_app', '0003_remove_aimodel_score_aidefect_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aidefect',
            name='xmax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aidefect',
            name='xmin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aidefect',
            name='ymax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aidefect',
            name='ymin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='expertdefect',
            name='xmax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='expertdefect',
            name='xmin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='expertdefect',
            name='ymax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='expertdefect',
            name='ymin',
            field=models.FloatField(),
        ),
    ]
