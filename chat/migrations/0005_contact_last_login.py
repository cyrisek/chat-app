# Generated by Django 4.1.3 on 2022-12-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_rename_username_contact_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
