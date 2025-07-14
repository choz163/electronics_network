from django.contrib import admin
from .models import NetworkNode, Product


@admin.action(description='Обнулить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    """
    Action для массового обнуления debt_to_supplier.
    """
    updated = queryset.update(debt_to_supplier=0)
    modeladmin.message_user(request, f'Задолженность обнулена у {updated} узлов.')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения NetworkNode в админке.
    """
    list_display = ('name', 'city', 'country', 'supplier_link', 'debt_to_supplier', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'city', 'country')
    actions = [clear_debt]
    readonly_fields = ('created_at',)

    def supplier_link(self, obj):
        """
        Отображает ссылку на поставщика в списке узлов.
        """
        if obj.supplier:
            url = f'/admin/core/networknode/{obj.supplier.pk}/change/'
            return f'<a href="{url}">{obj.supplier.name}</a>'
        return '-'
    supplier_link.allow_tags = True
    supplier_link.short_description = 'Поставщик'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения Product в админке.
    """
    list_display = ('title', 'model', 'node', 'release_date')
    list_filter = ('release_date', 'node__name')
    search_fields = ('title', 'model')
