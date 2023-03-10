# Generated by Django 4.1.5 on 2023-01-14 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='features_image_1',
            new_name='feature_image_1',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='features_image_2',
            new_name='feature_image_2',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='features_image_3',
            new_name='feature_image_3',
        ),
        migrations.AddField(
            model_name='product',
            name='feature_1_description',
            field=models.TextField(blank=True, max_length=2500),
        ),
        migrations.AddField(
            model_name='product',
            name='feature_2_description',
            field=models.TextField(blank=True, max_length=2500),
        ),
        migrations.AddField(
            model_name='product',
            name='feature_3_description',
            field=models.TextField(blank=True, max_length=2500),
        ),
    ]
