# Generated by Django 5.0.2 on 2024-04-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
