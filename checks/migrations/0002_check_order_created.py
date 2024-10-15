# Generated by Django 4.2.5 on 2023-10-22 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='order_created',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_created', to=settings.AUTH_USER_MODEL),
        ),
    ]