# Generated by Django 5.1.1 on 2024-09-14 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_remove_reply_message_remove_reply_responder_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=150)),
                ('content', models.TextField(max_length=1000)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Replied', 'Replied'), ('Spam', 'Spam')], default='Pending', max_length=20)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('replied_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_messages.message')),
                ('responder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userprofile')),
            ],
            options={
                'verbose_name': 'Reply',
                'verbose_name_plural': 'Replies',
            },
        ),
    ]
