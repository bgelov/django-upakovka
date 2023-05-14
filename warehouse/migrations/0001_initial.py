# Generated by Django 4.1.7 on 2023-05-09 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incoming_name', models.CharField(max_length=255, verbose_name='Название')),
                ('incoming_date', models.DateTimeField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'приход',
                'verbose_name_plural': 'Приход',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=255, verbose_name='Название')),
                ('order_date', models.DateTimeField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Название')),
                ('quantity_per_pallet', models.PositiveIntegerField(default=1, verbose_name='Штук на паллете')),
                ('barcode', models.CharField(blank=True, max_length=64, verbose_name='Штрихкод')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'продукцию',
                'verbose_name_plural': 'Продукция',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.product', verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Отгрузка продукции',
                'verbose_name_plural': 'Отгрузка продукции',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_product',
            field=models.ManyToManyField(through='warehouse.OrderProduct', to='warehouse.product'),
        ),
        migrations.CreateModel(
            name='IncomingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('incoming', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.incoming')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.product', verbose_name='Название')),
            ],
            options={
                'verbose_name': 'приход продукции',
                'verbose_name_plural': 'Приход продукции',
            },
        ),
        migrations.AddField(
            model_name='incoming',
            name='incoming_product',
            field=models.ManyToManyField(through='warehouse.IncomingProduct', to='warehouse.product'),
        ),
    ]