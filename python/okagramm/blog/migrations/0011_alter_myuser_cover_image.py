# Generated by Django 5.0.3 on 2024-03-21 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_myuser_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='cover_image',
            field=models.ImageField(default='user/setting/timeline-1.avif', upload_to='user/cover/'),
        ),
    ]
