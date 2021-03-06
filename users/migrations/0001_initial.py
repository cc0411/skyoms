# Generated by Django 3.1.2 on 2020-10-27 19:19

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRouter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=50, verbose_name='路由路径')),
                ('name', models.CharField(max_length=30, verbose_name='路由英文名称')),
                ('title', models.CharField(max_length=30, verbose_name='路由中文标题')),
                ('auth', models.BooleanField(default=True, verbose_name='是否需要验证')),
                ('component', models.CharField(max_length=50, verbose_name='路由关联的页面组件')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.permission', verbose_name='路由关联权限')),
            ],
            options={
                'verbose_name': '用户路由',
                'verbose_name_plural': '用户路由',
                'db_table': 'users_router',
            },
        ),
        migrations.CreateModel(
            name='UserMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=999, help_text='决定菜单显示顺序', verbose_name='菜单索引')),
                ('path', models.CharField(blank=True, max_length=50, null=True, verbose_name='菜单路径')),
                ('title', models.CharField(max_length=20, verbose_name='菜单名称')),
                ('icon', models.CharField(blank=True, max_length=20, null=True, verbose_name='菜单图标')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.usermenu', verbose_name='父级菜单')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.permission', verbose_name='菜单关联权限')),
            ],
            options={
                'verbose_name': '用户菜单',
                'verbose_name_plural': '用户菜单',
                'db_table': 'users_menu',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('image', models.ImageField(default='image/default.png', upload_to='image/%Y/%m', verbose_name='头像')),
                ('name', models.CharField(default='', max_length=32, verbose_name='姓名')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user_profile',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
