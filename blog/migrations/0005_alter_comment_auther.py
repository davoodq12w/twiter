# Generated by Django 5.0.2 on 2024-02-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_subject_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='auther',
            field=models.CharField(max_length=250),
        ),
    ]
