# Generated by Django 5.0.5 on 2024-07-10 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0003_alter_fooditem_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addtobag',
            old_name='item',
            new_name='food_item',
        ),
    ]