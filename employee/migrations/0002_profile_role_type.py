# Generated by Django 2.0.1 on 2019-06-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('hr', 'HR'), ('admin', 'Admin')], default='hr', max_length=10),
            preserve_default=False,
        ),
    ]
