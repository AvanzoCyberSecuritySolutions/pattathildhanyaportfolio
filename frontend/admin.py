from django.contrib import admin

# Register your models here.
from .models import HomeGalleryImage

@admin.register(HomeGalleryImage)
class HomeGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')
