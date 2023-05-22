from django.contrib import admin
from .models import Category, Product, Order, OrderProduct, Incoming, IncomingProduct
from import_export.admin import ImportExportModelAdmin


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 3
    # autocomplete_fields = ['product']

class OrderInProductPage(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('order', 'quantity', 'get_order_date')
    fields = readonly_fields

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class IncomingProductInline(admin.TabularInline):
    model = IncomingProduct
    extra = 3


class IncomingInProductPage(admin.TabularInline):
    model = IncomingProduct
    extra = 0
    readonly_fields = ('incoming', 'quantity', 'get_incoming_date')
    fields = readonly_fields

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product_name', 'category', 'quantity_per_pallet', 'barcode',)
    search_fields = ('product_name', 'barcode')
    inlines = [OrderInProductPage, IncomingInProductPage]
    ordering = ['product_name']

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ('order_name', 'order_date', 'get_products')
    list_filter = ['order_date']
    search_fields = ['order_name']

class IncomingAdmin(admin.ModelAdmin):
    inlines = [IncomingProductInline]
    list_display = ('incoming_name', 'incoming_date', 'get_products')
    list_filter = ['incoming_date']
    search_fields = ['incoming_name']
    ordering = ('-incoming_date',)


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('category_name', 'get_products')
    ordering = ('category_name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Incoming, IncomingAdmin)
