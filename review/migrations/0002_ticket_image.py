# Generated by Django 4.2.1 on 2023-07-21 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(default=None, upload_to='ticket_images/'),
            preserve_default=False,
        ),
    ]
