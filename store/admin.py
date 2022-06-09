from django.contrib import admin
from store.models import Category,Product,Cart,CartItem,Order,OrderItem,image_product,Contact
# Register your models here.

class imageStackedInline(admin.StackedInline):
    model = image_product

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','created','updated']
    list_editable=['price','stock']
    list_per_page=5
    list_filter = ['name','price']
    search_fields = ['name']
    inlines = [imageStackedInline]

class CategoryAdmin(admin.ModelAdmin):
     list_display =  ['name','slug']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)
