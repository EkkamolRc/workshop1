# Generated by Django 3.2.4 on 2022-05-15 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220512_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('token', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ('date_add',), 'verbose_name': 'ตะกร้าสินค้า', 'verbose_name_plural': 'ข้อมูลตะกร้าสินค้า'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'รายการสินค้าในตะกร้า', 'verbose_name_plural': 'ข้อมูลรายการสินค้าในตะกร้า'},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
    ]
