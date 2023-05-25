from django.db.models import Sum

from warehouse.models import OrderProduct, Order


def print_order_result(object_id):
    order_table = OrderProduct.objects.filter(order_id=object_id).select_related('product').values('product__barcode', 'product__product_name', 'quantity')
    product_sum = order_table.aggregate(Sum('quantity'))

    result = {
        'order_table': order_table,
        'product_sum': product_sum,
    }

    return result

def order_info(object_id):
    result = Order.objects.filter(id=object_id).values('order_name', 'order_date')
    return result[0]