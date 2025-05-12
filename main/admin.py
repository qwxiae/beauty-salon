from django.contrib import admin
from .models import Product, Category, Discount, \
    ProductImage, Specialist, ProductSpecialist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductSpecialistInline(admin.TabularInline):
    model = ProductSpecialist
    extra = 3


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "price",
        "category",
        "stock",
        "is_available",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_available", "category")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    inlines = [ProductImageInline, ProductSpecialistInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    # Category and product are passed into list_display by default
    list_display = (
        "name",
        "slug",
        "percentage",
        "start_date",
        "end_date",
    )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("end_date",)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
