
from django.urls import path
from . import views

urlpatterns = [
    path('',views.BlogHomePage.as_view(),name='bhome'),
    path('blogpost/<int:id>',views.blogpost,name='blogpost'),
]