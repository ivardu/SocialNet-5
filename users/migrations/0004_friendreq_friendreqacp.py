# Generated by Django 2.2 on 2020-01-18 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200114_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendReqAcp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.CharField(default='no', max_length=3)),
                ('auser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_req', models.CharField(default='no', max_length=3)),
                ('fracp', models.ManyToManyField(to='users.FriendReqAcp')),
                ('ruser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]