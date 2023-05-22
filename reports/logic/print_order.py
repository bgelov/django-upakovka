from warehouse.models import OrderProduct, Order


def print_order_result(object_id):
    result = OrderProduct.objects.filter(order_id=object_id).select_related('product').values('product__barcode', 'product__product_name', 'quantity')
    return result

def order_info(object_id):
    result = Order.objects.filter(id=object_id).values('order_name', 'order_date')
    return result[0]