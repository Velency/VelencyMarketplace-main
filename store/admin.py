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
admin.site.register(Stream)



class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_teachers', 'Category')

    def display_teachers(self, obj):
        return ", ".join([teacher.first_name for teacher in obj.teachers.all()])
    display_teachers.short_description = 'Teachers'


admin.site.register(Course, CourseAdmin)


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


class VideoRecInline(admin.TabularInline):
    fk_name = 'Lesson'
    model = VideoRec


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [VideoRecInline,]


class Sub_CategoryInline(admin.TabularInline):
    fk_name = 'category'
    model = Sub_Category


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    inlines = [Sub_CategoryInline,]
