import numpy as np
import pandas as pd

from reports.logic.report_func import get_order_products_sum, get_incoming_products_sum


def pallet_only_report_result(products, date_range):
    products_count = products.count()
    result = pd.DataFrame(products)
    result_pallet_only = pd.DataFrame(products)

    if products_count > 0:
        for d in date_range:
            filter_date = d.replace(hour=23, minute=59, second=59)
            filter_date_col = d.strftime('%d/%m/%Y')

            incoming_products = pd.DataFrame(get_incoming_products_sum(filter_date))
            if len(incoming_products.index) == 0:
                result[f'total incoming {filter_date_col}'] = [0] * products_count
            else:
                result = result.merge(incoming_products, left_on='id', right_on='product_id', how='left')
                result[f'total incoming {filter_date_col}'] = (result['total_incoming']).astype('Int64')
                result.drop('total_incoming', axis=1, inplace=True)
                result.drop('product_id', axis=1, inplace=True)

            order_products = pd.DataFrame(get_order_products_sum(filter_date))
            if len(order_products.index) == 0:
                result[f'total order {filter_date_col}'] = [0] * products_count
            else:
                result = result.merge(order_products, left_on='id', right_on='product_id', how='left')
                result[f'total order {filter_date_col}'] = (result['total_order']).astype('Int64')
                result.drop('total_order', axis=1, inplace=True)
                result.drop('product_id', axis=1, inplace=True)

            result.fillna(0, inplace=True)

            result[f'incoming minus order {filter_date_col}'] = (result[f'total incoming {filter_date_col}'] - result[f'total order {filter_date_col}']).astype('Int64')

            if len(order_products.index) == 0:
                # https://stackoverflow.com/questions/27592456/floor-or-ceiling-of-a-pandas-series-in-python
                result_pallet_only[filter_date_col] = np.ceil(
                    result[f'total incoming {filter_date_col}'] / result['quantity_per_pallet']
                ).astype('Int64')
            else:
                result_pallet_only[filter_date_col] = np.ceil(
                    (result[f'total incoming {filter_date_col}'] - result[f'total order {filter_date_col}']) / result['quantity_per_pallet']
                ).astype('Int64')

            result_pallet_only.fillna(0, inplace=True)
    return result_pallet_only