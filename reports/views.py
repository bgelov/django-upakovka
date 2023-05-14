from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# https://docs.djangoproject.com/en/4.2/topics/auth/default/
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone

from warehouse.models import Product, Category, IncomingProduct, OrderProduct

# For pandas report export
from io import BytesIO
from django.http import HttpResponse


def get_filter_date(request):
    if request.method == 'POST' and request.POST.get('filter_date_start') != '' and request.POST.get(
            'filter_date_end') != '':
        filter_date_start = datetime.strptime(request.POST.get('filter_date_start'), '%Y-%m-%d')
        filter_date_end = datetime.strptime(request.POST.get('filter_date_end'), '%Y-%m-%d')

    else:
        filter_date_end = datetime.now()
        filter_date_start = filter_date_end - timedelta(days=7)

    # https://stackoverflow.com/questions/8361099/django-python-date-time-set-to-midnight
    # filter_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    filter_date_start = filter_date_start.replace(hour=0, minute=0, second=0, microsecond=0)
    filter_date_end = filter_date_end.replace(hour=23, minute=59, second=59, microsecond=99999)
    return [filter_date_start, filter_date_end]


def get_date_range(filter_date_start, filter_date_end):
    # https://pandas.pydata.org/docs/reference/api/pandas.date_range.html
    # date_range = pd.date_range(start='1/1/2023', end='4/1/2023')
    date_range = pd.date_range(
        start=pd.to_datetime(filter_date_start).tz_localize("Europe/Moscow"),
        end=pd.to_datetime(filter_date_end).tz_localize("Europe/Moscow"),
    )
    return date_range


def products_and_category():
    products = Product.objects.all().select_related('category').values(
        'id', 'product_name', 'category__category_name', 'quantity_per_pallet'
    )
    return products


def get_order_products_sum(filter_date):
    order_products_sum = OrderProduct.objects.values(
        'product_id'
    ).filter(
        order__order_date__lte=filter_date
    ).order_by(
        'product_id'
    ).annotate(
        total_order=Sum('quantity'))
    return order_products_sum


def get_incoming_products_sum(filter_date):
    incoming_products_sum = IncomingProduct.objects.values(
        'product_id'
    ).filter(
        incoming__incoming_date__lte=filter_date
    ).order_by(
        'product_id'
    ).annotate(
        total_incoming=Sum('quantity'))
    return incoming_products_sum


def export_to_excel(result, export_file_name='export'):
    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            result.to_excel(writer, sheet_name="Data", index=False)
        filename = f"{export_file_name}.xlsx"
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.ms-excel'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res

def index_report(request):
    return render(request, 'reports/index.html')


def pallet_report_result(products, date_range):
    products_count = products.count()
    result = pd.DataFrame(products)

    if products_count > 0:
        for d in date_range:
            filter_date = d.replace(hour=23, minute=59, second=59)
            filter_date_col = d.strftime('%d/%m/%Y')

            order_products = pd.DataFrame(get_order_products_sum(filter_date))
            order_products.fillna(0, inplace=True)

            incoming_products = pd.DataFrame(get_incoming_products_sum(filter_date))
            incoming_products.fillna(0, inplace=True)

            if len(order_products.index) == 0:
                order_products['total_order'] = [0] * products_count
            if len(incoming_products.index) == 0:
                incoming_products['total_incoming'] = [0] * products_count

            result[f'total incoming {filter_date_col}'] = incoming_products['total_incoming']
            result[f'total order {filter_date_col}'] = order_products['total_order']
            result[f'incoming minus order {filter_date_col}'] = incoming_products['total_incoming'] - order_products['total_order']

            if len(order_products.index) == 0:
                # https://stackoverflow.com/questions/27592456/floor-or-ceiling-of-a-pandas-series-in-python
                result[filter_date_col] = np.ceil(
                    incoming_products['total_incoming'] / result['quantity_per_pallet']
                ).astype('Int64')
            else:
                result[filter_date_col] = np.ceil(
                    (incoming_products['total_incoming'] - order_products['total_order']) / result[
                        'quantity_per_pallet']
                ).astype('Int64')

            result.fillna(0, inplace=True)
    return result

@login_required
def pallet_report(request):
    template = 'reports/pallet.html'
    report_name = 'Приход, расход, разница и количество паллет по датам.'

    filter_date_start, filter_date_end = get_filter_date(request)
    date_range = get_date_range(filter_date_start, filter_date_end)
    products = products_and_category()
    result = pallet_report_result(products, date_range)

    context = {
        'report_name': report_name,
        'df': result.to_html(),
        'products_count': products.count(),
        'filter_date_start': filter_date_start,
        'filter_date_end': filter_date_end,
    }
    return render(request, template, context)


@login_required
def pallet_report_export(request):
    filter_date_start, filter_date_end = get_filter_date(request)
    date_range = get_date_range(filter_date_start, filter_date_end)
    products = products_and_category()
    result = pallet_report_result(products, date_range)
    return export_to_excel(result, 'pallet_report_export')


# https://stackoverflow.com/questions/45547674/how-to-execute-a-group-by-count-or-sum-in-django-orm
def inventory_report(request):
    """
    Report Inventory
    All products and how many pieces of products on the warehouse
    """
    template = 'reports/inventory.html'
    filter_date = timezone.now()

    products = Product.objects.all().values()
    df_product = pd.DataFrame(products)

    order_products_sum = OrderProduct.objects.values(
        'product_id'
    ).filter(
        order__order_date__lte=filter_date
    ).order_by(
        'product_id'
    ).annotate(
        total_order=Sum('quantity'))
    order_products = pd.DataFrame(order_products_sum)

    incoming_products_sum = IncomingProduct.objects.values(
        'product_id'
    ).filter(
        incoming__incoming_date__lte=filter_date
    ).order_by(
        'product_id'
    ).annotate(
        total_incoming=Sum('quantity'))
    incoming_products = pd.DataFrame(incoming_products_sum)

    result = df_product.merge(
        incoming_products,
        left_on='id', right_on='product_id'
    ).merge(
        order_products,
        left_on='id', right_on='product_id')

    result['total_now'] = result['total_incoming'] - result['total_order']

    context = {
        'df': result.to_html(),
        'filter_date': filter_date
    }

    return render(request, template, context)


def products_report(request):
    template = 'reports/products.html'
    # context = {}
    # context = Product.objects.all()
    # quantity_incoming = IncomingProduct.objects.all().quantity
    context = {'products': Product.objects.all()}
    return render(request, template, context)


def export_report_pallet(request):
    filter_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    products = Product.objects.all().select_related('category').values()
    products_count = Product.objects.all().count()

    df_product = pd.DataFrame(products)
    result = df_product

    # https://pandas.pydata.org/docs/reference/api/pandas.date_range.html
    # Without timezone:
    # date_range = pd.date_range(start='1/1/2023', end='4/1/2023')
    date_range = pd.date_range(
        start=pd.to_datetime('3/20/2023').tz_localize("Europe/Moscow"),
        end=pd.to_datetime('4/9/2023').tz_localize("Europe/Moscow"),
    )

    for d in date_range:
        filter_date = d
        filter_date_col = d.strftime('%d/%m/%Y')

        order_products_sum = OrderProduct.objects.values(
            'product_id'
        ).filter(
            order__order_date__lte=filter_date
        ).order_by(
            'product_id'
        ).annotate(
            total_order=Sum('quantity'))
        order_products = pd.DataFrame(order_products_sum)
        order_products.fillna(0, inplace=True)
        # print(order_products)

        incoming_products_sum = IncomingProduct.objects.values(
            'product_id'
        ).filter(
            incoming__incoming_date__lte=filter_date
        ).order_by(
            'product_id'
        ).annotate(
            total_incoming=Sum('quantity'))
        incoming_products = pd.DataFrame(incoming_products_sum)
        incoming_products.fillna(0, inplace=True)
        # print(incoming_products)

        if len(order_products.index) == 0:
            order_products['total_order'] = [0] * products_count
        if len(incoming_products.index) == 0:
            incoming_products['total_incoming'] = [0] * products_count

        # result[f'total incoming {filter_date}'] = incoming_products['total_incoming']
        # result[f'total order {filter_date}'] = order_products['total_order']

        if len(order_products.index) == 0:
            # https://stackoverflow.com/questions/27592456/floor-or-ceiling-of-a-pandas-series-in-python
            result[filter_date_col] = np.ceil(
                incoming_products['total_incoming'] / df_product['quantity_per_pallet']
            ).astype('Int64')
        else:
            result[filter_date_col] = np.ceil(
                (incoming_products['total_incoming'] - order_products['total_order']) / df_product[
                    'quantity_per_pallet']
            ).astype('Int64')

        result.fillna(0, inplace=True)

    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            result.to_excel(writer, sheet_name="Data", index=False)

        filename = f"pallet_report.xlsx"
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.ms-excel'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res
