# Generated by Django 4.2.7 on 2024-04-07 03:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Text', 'Text'), ('File', 'File')], default='Text', max_length=25)),
                ('content', models.TextField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='conversations.conversation')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='users.user')),
            ],
        ),
    ]