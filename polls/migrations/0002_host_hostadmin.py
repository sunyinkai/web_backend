# Generated by Django 2.1.3 on 2018-11-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32)),
                ('port', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HostAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
                ('host', models.ManyToManyField(to='polls.Host')),
            ],
        ),
    ]