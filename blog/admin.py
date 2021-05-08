from django.contrib import admin
from .models import Blog_post

# Register your models here.

@admin.register(Blog_post)
class Blog_postModelAdmin(admin.ModelAdmin):
    list_display=['id','title','description']