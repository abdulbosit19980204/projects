# Generated by Django 5.0.2 on 2024-03-06 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.tag'),
        ),
    ]