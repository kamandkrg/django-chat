# Generated by Django 3.2 on 2022-09-18 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_privatechatroom_user2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.statusmessage'),
        ),
    ]
