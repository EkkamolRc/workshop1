# Generated by Django 4.0.5 on 2022-06-09 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(help_text='example@gmail.com', max_length=250)),
                ('comment', models.TextField(max_length=255)),
            ],
        ),
    ]
