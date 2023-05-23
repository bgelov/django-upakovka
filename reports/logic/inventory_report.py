import pandas as pd

from reports.logic.report_func import get_order_products_sum, get_incoming_products_sum


def inventory_report_result(products, filter_date):
    """
    Calculate inventory report
    """
    products_count = products.count()
    result = pd.DataFrame(products)
    filter_date_col = filter_date.strftime('%d/%m/%Y %H:%M:%S')

    if products_count > 0:

        incoming_products = pd.DataFrame(get_incoming_products_sum(filter_date))
        if len(incoming_products.index) == 0:
            result['total_incoming'] = [0] * products_count
        else:
            incoming_products.fillna(0, inplace=True)
            result = result.merge(incoming_products, left_on='id', right_on='product_id', how='left')
            result.drop('product_id', axis=1, inplace=True)

        order_products = pd.DataFrame(get_order_products_sum(filter_date))
        if len(order_products.index) == 0:
            result['total_order'] = [0] * products_count
        else:
            order_products.fillna(0, inplace=True)
            result = result.merge(order_products, left_on='id', right_on='product_id', how='left')
            result.drop('product_id', axis=1, inplace=True)

        result.fillna(0, inplace=True)

        result['total_now_' + str(filter_date_col)] = (result['total_incoming'] - result['total_order']).astype('Int64')

    return result
