# Generated by Django 2.0 on 2017-12-12 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.CharField(blank=True, max_length=67)),
                ('role', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=200)),
                ('question_body', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qanda.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qanda.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_answered',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qanda.Question'),
        ),
    ]
