# Generated by Django 2.0.7 on 2018-07-16 17:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateTimeField()),
                ('temperature', models.FloatField()),
                ('humidity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this device', primary_key=True, serialize=False)),
                ('device_info', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='data',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devicedata.Device'),
        ),
    ]