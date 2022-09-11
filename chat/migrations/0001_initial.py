# Generated by Django 3.1.12 on 2022-09-11 09:47

import chat.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateChatRoom',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=64)),
                ('receiver', models.CharField(max_length=64, unique=True)),
                ('message', djongo.models.fields.ArrayField(model_container=chat.models.Message)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('modify_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
