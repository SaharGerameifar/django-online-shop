# Generated by Django 3.2.12 on 2022-04-05 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.province'),
        ),
    ]
