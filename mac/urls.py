"""mac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from . import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage.as_view(),name='mhome'),
    path('blog/',include('blog.urls')),
    path('shop/',include('shop.urls')),
    path('prac/',views.prac, name='prac'),
    path("Json/",views.jsondata,name = "jsondata"),

    path('signup/', views.signup, name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),   ## now url_path = /login/ not accounts/login/
    # path('dashboard/', views.UserProfile.as_view(), name="dashboard"), ## classed view
    path('logout/', views.MyLogoutView.as_view(), name='logout'), ## now url_path = /logout/ not accounts/logout/
    path('changepass/', views.MyPasswordChangeView.as_view(), name='changepass'), 
    path('password_change_done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
