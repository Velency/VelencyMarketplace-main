from django.contrib import admin
from .models import *


admin.site.register(Slider)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Trend)
admin.site.register(WishItem)
admin.site.register(Customer)
admin.site.register(Comments)
admin.site.register(Offer)
admin.site.register(Support)
admin.site.register(Withdraw)


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [GalleryInline,]



class Sub_CategoryInline(admin.TabularInline):
    fk_name = 'category'
    model = Sub_Category


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    inlines = [Sub_CategoryInline,]



