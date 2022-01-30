from django.contrib import admin

# Register your models here.
from seller.models import Message, Reply, Staff, Store, Seller


class Seller_(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname']
    list_per_page = 20


class Staff_(admin.ModelAdmin):
    list_filter = ['type', 'update', 'storeid']

    def change_normal(self, request, queryset):
        queryset.update(status=1)

    change_normal.short_description = "正常"

    def change_short(self, request, queryset):
        queryset.update(status=2)

    change_short.short_description = "缺货"

    def change_dell(self, request, queryset):
        queryset.update(status=3)

    change_dell.short_description = "删除"

    def change_down(self, request, queryset):
        queryset.update(status=4)

    change_down.short_description = "下架"
    actions = [change_dell, change_down, change_normal, change_short]


class Store_(admin.ModelAdmin):
    list_filter = ['sellerid']


admin.site.register(Seller, Seller_)
admin.site.register(Store, Store_)
admin.site.register(Staff, Staff_)
admin.site.register(Reply)
admin.site.register(Message)
