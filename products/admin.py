from django.contrib import admin
from .models import Category, Product, Tag, ProductImageGallery, Comment, Slider, Like, Save, IPAddress, ProductHit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub', 'position', 'status')
    list_filter = (['status', 'is_sub'])
    search_fields = (['name'])
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category','image_gallery', 'tag', 'related_product')
    list_display = ('name', 'available')
    list_filter = (['available',])
    search_fields = (['name'])
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = (['name'])
    prepopulated_fields = {'slug': ('name',)}    


@admin.register(ProductImageGallery)
class ProductImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = (['name'])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'is_reply', 'created', 'is_active')   
    raw_id_fields = ('user', 'product', 'reply')    


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('name', )   


admin.site.register(Like)

admin.site.register(Save)

admin.site.register(IPAddress)

admin.site.register(ProductHit)