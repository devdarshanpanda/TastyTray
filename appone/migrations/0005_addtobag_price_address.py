# Generated by Django 5.0.5 on 2024-07-10 06:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0004_rename_item_addtobag_food_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtobag',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.BigIntegerField()),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
