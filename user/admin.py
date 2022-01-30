from django.contrib import admin
# Register your models here.
from user.models import Expression, User, Address, Order, Cart, His


class User_(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname']
    list_per_page = 20


class Order_(admin.ModelAdmin):
    fieldsets = (
        ("买家信息", {"fields": ['user', 'userid', 'address', 'buy_number']}),
        ("卖家信息", {"fields": ['seller']}),
        ("商品信息", {"fields": ['name', 'staff', 'price', 'store', 'number', 'pictere']}),
        ("订单", {"fields": ['status']}),
    )


admin.site.register(User, User_)
admin.site.register(Expression)
admin.site.register(Address)
admin.site.register(Order,Order_)
admin.site.register(Cart)
admin.site.register(His)