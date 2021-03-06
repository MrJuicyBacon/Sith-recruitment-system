# Generated by Django 2.2.6 on 2019-10-25 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sith', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='recruit',
            name='assigned_sith',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sith.Sith'),
        ),
        migrations.CreateModel(
            name='TestAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=1000)),
                ('questions', models.ManyToManyField(to='sith.Question')),
            ],
        ),
        migrations.CreateModel(
            name='CollectedResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Question')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Recruit')),
            ],
        ),
    ]
