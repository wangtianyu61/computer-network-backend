# Generated by Django 3.1 on 2020-10-19 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('entry_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('author', models.TextField(null=True)),
                ('price', models.FloatField()),
                ('original_price', models.FloatField(null=True)),
                ('category', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('customer_inventory', models.IntegerField()),
                ('seller_inventory', models.IntegerField()),
                ('status', models.IntegerField()),
                ('seller_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'Entry',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('serial', models.BigIntegerField()),
                ('customer_id', models.BigIntegerField()),
                ('order_time', models.DateTimeField()),
                ('postageFee', models.FloatField()),
                ('paymentType', models.IntegerField()),
            ],
            options={
                'db_table': 'OrderInfo',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('avatar', models.TextField(null=True)),
                ('real_name', models.TextField()),
                ('age', models.IntegerField(null=True)),
                ('sex', models.IntegerField(null=True)),
                ('certificationType', models.IntegerField(null=True)),
                ('certificationNumber', models.BigIntegerField(null=True)),
                ('address', models.TextField()),
                ('username', models.TextField()),
                ('password', models.TextField()),
                ('telephone', models.TextField()),
            ],
            options={
                'db_table': 'UserInfo',
            },
        ),
        migrations.CreateModel(
            name='UserAccountType',
            fields=[
                ('serial_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('payment_type', models.TextField()),
                ('account_id', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userinfo')),
            ],
            options={
                'db_table': 'UserAccountType',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.BigIntegerField()),
                ('number', models.IntegerField()),
                ('seller_id', models.BigIntegerField()),
                ('deliver_time', models.DateTimeField(null=True)),
                ('postageFee', models.FloatField()),
                ('status', models.IntegerField()),
                ('receiveType', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.orderinfo')),
            ],
            options={
                'db_table': 'OrderDetail',
            },
        ),
        migrations.CreateModel(
            name='AfterSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aftersale_post', models.TextField()),
                ('post_time', models.DateTimeField()),
                ('aftersale_feedback', models.TextField(null=True)),
                ('feedback_time', models.DateTimeField(null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.orderinfo')),
            ],
        ),
        migrations.CreateModel(
            name='EntryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.IntegerField()),
                ('image', models.TextField()),
                ('entry_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.entry')),
            ],
            options={
                'db_table': 'EntryImage',
                'unique_together': {('entry_id', 'image_id')},
            },
        ),
        migrations.CreateModel(
            name='EntryComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_comment_id', models.IntegerField()),
                ('entry_comment', models.TextField()),
                ('comment_time', models.DateTimeField()),
                ('entry_feedback', models.TextField()),
                ('entry_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.entry')),
            ],
            options={
                'db_table': 'EntryComment',
                'unique_together': {('entry_id', 'entry_comment_id')},
            },
        ),
    ]
