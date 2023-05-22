from django.urls import path

from .views import index_report, inventory_report, pallet_report, pallet_only_report, export_report_inventory, \
    export_report_pallet, \
    export_report_pallet_only, print_order

app_name = 'reports'
urlpatterns = [
    path('', index_report, name='index_report'),
    path('inventory/', inventory_report, name='inventory_report'),
    path('pallet/', pallet_report, name='pallet_report'),
    path('pallet-only/', pallet_only_report, name='pallet_only_report'),
    path('export-report-inventory/', export_report_inventory, name='export_report_inventory'),
    path('export-report-pallet/', export_report_pallet, name='export_report_pallet'),
    path('export-report-pallet-only/', export_report_pallet_only, name='export_report_pallet_only'),
    path('print-order/<int:object_id>', print_order, name='print_order'),
]

