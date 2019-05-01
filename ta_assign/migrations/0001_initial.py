# Generated by Django 2.1.7 on 2019-04-30 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=10)),
                ('num_labs', models.IntegerField(default=0)),
                ('instructor', models.CharField(default='no Instructor', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TACourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(default='000.000.0000', max_length=12)),
                ('name', models.CharField(default='DEFAULT', max_length=50)),
                ('type', models.CharField(default='person', max_length=20)),
                ('isLoggedOn', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='tacourse',
            name='TA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_assign.User'),
        ),
        migrations.AddField(
            model_name='tacourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_assign.Course'),
        ),
    ]