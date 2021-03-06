# Generated by Django 2.2.11 on 2020-06-13 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolmanager',
            name='classes',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='classes.Class'),
        ),
        migrations.AlterField(
            model_name='schoolmanager',
            name='subject',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.Student'),
        ),
    ]
