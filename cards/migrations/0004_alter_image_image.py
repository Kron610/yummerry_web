# Generated by Django 4.2 on 2023-05-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='upload/'),
        ),
    ]
