# Generated by Django 4.2.1 on 2023-06-14 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_remove_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=20),
        ),
    ]
