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
admin.site.register(TeamMember)
admin.site.register(NewsFeed)
admin.site.register(Partnership)
admin.site.register(packagesCat)
admin.site.register(Packages)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'Category')
    list_filter = ('Category',)  # Добавляем фильтр по категории
    # Добавляем поиск по имени, фамилии преподавателя
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')
    # Другие настройки админки для Course, если необходимо


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # Добавляем возможность выбора курсов через горизонтальное поле
    filter_horizontal = ('courses',)
    # Другие настройки админки для Direction, если необходимо


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
