# Generated by Django 4.0.4 on 2022-05-12 10:19

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=ckeditor.fields.RichTextField(max_length=5000, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='replie',
            name='reply_content',
            field=ckeditor.fields.RichTextField(max_length=5000, verbose_name=''),
        ),
    ]
