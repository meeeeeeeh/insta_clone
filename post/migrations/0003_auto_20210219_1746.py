# Generated by Django 3.1.6 on 2021-02-19 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20210219_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ManyToManyField(related_name='contents', to='post.PostFileContent'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='post.Tag'),
        ),
    ]
