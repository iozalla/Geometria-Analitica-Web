# Generated by Django 4.0.2 on 2022-02-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
