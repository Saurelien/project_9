# Generated by Django 4.2.1 on 2023-08-28 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='display_order',
        ),
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.TextField(blank=True, default='', max_length=8192),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_images/'),
        ),
    ]
