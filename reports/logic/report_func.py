from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone

from warehouse.models import Product, OrderProduct, IncomingProduct


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
        total_order=Sum('quantity', default=0))
    return order_products_sum


def get_incoming_products_sum(filter_date):
    incoming_products_sum = IncomingProduct.objects.values(
        'product_id'
    ).filter(
        incoming__incoming_date__lte=filter_date
    ).order_by(
        'product_id'
    ).annotate(
        total_incoming=Sum('quantity', default=0))
    return incoming_products_sum


def export_to_excel(result, export_file_name='export'):
    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            result.to_excel(writer, sheet_name="Data", index=False)
        filename = f"{export_file_name}_{timezone.now().strftime('%d_%m_%Y-%H_%M_%S')}.xlsx"
        xlsx_output = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.ms-excel'
        )
        xlsx_output['Content-Disposition'] = f'attachment; filename={filename}'
        return xlsx_output
