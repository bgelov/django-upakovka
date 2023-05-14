from django.urls import path

from .views import inventory_report, pallet_report, products_report, export_report_pallet

app_name = 'reports'
urlpatterns = [
    path('inventory/', inventory_report),
    path('pallet/', pallet_report, name='pallet_report'),
    path('export_report_pallet/', export_report_pallet),
    path('products/', products_report),
]

