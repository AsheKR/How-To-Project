# Generated by Django 2.1.5 on 2019-02-09 12:25

from django.db import migrations, models
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.CharField(max_length=15, unique=True, verbose_name='유저아이디')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='유저이메일')),
                ('nickname', models.CharField(max_length=15, verbose_name='별명')),
                ('description', models.TextField(blank=True, null=True, verbose_name='자기소개')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='프로필 이미지')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': ('유저',),
                'verbose_name_plural': ('유저',),
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]