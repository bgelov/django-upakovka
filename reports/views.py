# https://docs.djangoproject.com/en/4.2/topics/auth/default/
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone

from reports.logic.inventory_report import inventory_report_result
from reports.logic.pallet_only_report import pallet_only_report_result
from reports.logic.pallet_report import pallet_report_result
from reports.logic.print_order import print_order_result, order_info
from reports.logic.report_func import get_filter_date, get_date_range, products_and_category, export_to_excel
from warehouse.models import Product, Category, IncomingProduct, OrderProduct

import numpy as np
import pandas as pd

# For pandas report export
from io import BytesIO

from django.http import HttpResponse


# Index page =======================================================================

@login_required
def index_report(request):
    # Index page for reports
    return render(request, 'reports/index.html')

# End index page ===================================================================

# Inventory report =======================================================================

@login_required
def inventory_report(request, export=False):
    """
    Report Inventory
    All products and how many pieces of products on the warehouse
    """
    template = 'reports/inventory.html'
    report_name = 'Остатки продукции'

    filter_date = timezone.now()
    products = products_and_category()
    result = inventory_report_result(products, filter_date)

    if export:
        return export_to_excel(result, 'inventory_report_export')

    context = {
        'report_name': report_name,
        'df': result.to_html(index=False),
        'products_count': products.count(),
        'filter_date': filter_date,
        'export_link': 'export-report-inventory',
    }
    return render(request, template, context)


@login_required
def export_report_inventory(request):
    return inventory_report(request, True)

# End inventory report ====================================================================


# Pallet report =======================================================================

@login_required
def pallet_report(request, export=False):
    template = 'reports/pallet.html'
    report_name = 'Количество паллет по датам, приход, расход, разница'

    filter_date_start, filter_date_end = get_filter_date(request)
    date_range = get_date_range(filter_date_start, filter_date_end)
    products = products_and_category()
    result = pallet_report_result(products, date_range)

    if export:
        return export_to_excel(result, 'pallet_report_export')

    context = {
        'report_name': report_name,
        'df': result.to_html(index=False),
        'products_count': products.count(),
        'filter_date_start': filter_date_start,
        'filter_date_end': filter_date_end,
        'export_link': 'export-report-pallet',
    }
    return render(request, template, context)


@login_required
def export_report_pallet(request):
    return pallet_report(request, True)


# End pallet report ====================================================================


# Pallet only report ===================================================================

@login_required
def pallet_only_report(request, export=False):
    template = 'reports/pallet.html'
    report_name = 'Количество паллет по датам'

    filter_date_start, filter_date_end = get_filter_date(request)
    date_range = get_date_range(filter_date_start, filter_date_end)
    products = products_and_category()
    result = pallet_only_report_result(products, date_range)

    if export:
        return export_to_excel(result, 'pallet_only_report_export')

    context = {
        'report_name': report_name,
        'df': result.to_html(index=False),
        'products_count': products.count(),
        'filter_date_start': filter_date_start,
        'filter_date_end': filter_date_end,
        'export_link': 'export-report-pallet-only',
    }
    return render(request, template, context)


@login_required
def export_report_pallet_only(request):
    return pallet_only_report(request, True)

# End pallet only report ===============================================================


# Print order ==========================================================================

@login_required
def print_order(request, object_id):
    template = 'reports/print_order.html'
    report_name = 'Печать заказа'

    result = print_order_result(object_id)
    order = order_info(object_id)

    context = {
        'report_name': report_name,
        'order_info': order,
        'result': result,
    }
    return render(request, template, context)

# End print order ======================================================================