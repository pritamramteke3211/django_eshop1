from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    list_display = ['post_id','title','category','pub_date']