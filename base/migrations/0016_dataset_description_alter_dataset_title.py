# Generated by Django 5.1.6 on 2025-05-29 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_datasetimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
