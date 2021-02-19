# Generated by Django 3.1.6 on 2021-02-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ManyToManyField(blank=True, null=True, related_name='contents', to='post.PostFileContent'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='post.Tag'),
        ),
    ]