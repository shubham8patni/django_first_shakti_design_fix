# Generated by Django 4.0.3 on 2022-06-06 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0005_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]