# Generated by Django 5.0.4 on 2024-11-22 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_view', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Hashtags',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Post_hashtags',
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]