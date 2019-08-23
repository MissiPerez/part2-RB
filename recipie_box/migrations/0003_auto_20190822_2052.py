# Generated by Django 2.2.4 on 2019-08-22 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipie_box', '0002_recipie_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipie',
            name='favorite',
        ),
        migrations.AddField(
            model_name='author',
            name='favorite',
            field=models.ManyToManyField(related_name='favorite', to='recipie_box.Recipie'),
        ),
    ]
