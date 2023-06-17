from django.db.models import Sum

from warehouse.models import IncomingProduct, Incoming


def print_incoming_result(object_id):
    incoming_table = IncomingProduct.objects.filter(incoming_id=object_id).select_related('product').values('product__barcode', 'product__product_name', 'quantity')
    product_sum = incoming_table.aggregate(Sum('quantity'))

    result = {
        'incoming_table': incoming_table,
        'product_sum': product_sum,
    }

    return result

def incoming_info(object_id):
    result = Incoming.objects.filter(id=object_id).values('incoming_name', 'incoming_date')
    return result[0]