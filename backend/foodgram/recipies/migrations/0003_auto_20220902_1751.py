# Generated by Django 2.2.19 on 2022-09-02 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0002_auto_20220902_1710'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_user_recipe',
        ),
    ]
