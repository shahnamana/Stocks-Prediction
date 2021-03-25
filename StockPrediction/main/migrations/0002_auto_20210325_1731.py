# Generated by Django 3.1.5 on 2021-03-25 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boughtStocks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Investor',
        ),
    ]
