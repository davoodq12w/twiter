# Generated by Django 5.0.2 on 2024-02-28 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_comment_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0, max_length=250),
        ),
    ]
