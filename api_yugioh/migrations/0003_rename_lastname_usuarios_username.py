# Generated by Django 5.1.3 on 2024-11-16 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_yugioh', '0002_rename_confirmpassword_usuarios_password2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarios',
            old_name='lastname',
            new_name='username',
        ),
    ]