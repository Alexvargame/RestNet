# Generated by Django 4.2.5 on 2023-10-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('seller', 'seller'), ('client', 'client'), ('courier', 'courier')], max_length=100),
        ),
    ]