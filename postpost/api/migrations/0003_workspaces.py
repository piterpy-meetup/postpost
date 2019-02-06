# Generated by Django 2.1.5 on 2019-02-06 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20190128_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('publisher', 'Publisher: only create and edit publications'), ('admin', 'Admin: also can edit platforms and members')], default='publisher', max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Workspace')),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='workspace',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Workspace'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='workspacemember',
            unique_together={('member', 'workspace')},
        ),
    ]