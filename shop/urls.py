
from django.urls import path
from . import views


urlpatterns = [
    path('',views.ShopHomePage.as_view(),name='home'),
    path('dashboard/', views.UserProfile.as_view(), name="dashboard"), ## classed view
    path('add_to_cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('buy_now/<int:product_id>/',views.buy_now,name='buy_now'),
    path('mycart/',views.mycart,name='mycart'),
    # path('checkout/',views.checkout,name='checkout'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),

    path('address/',views.address,name='address'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),
  


    path('productview/<int:product_id>', views.productview,name="productview"),
    path('quantity_plus/<int:cart_id>', views.quantity_plus,name='quantity_plus'),
    path('quantity_minus/<int:cart_id>', views.quantity_minus,name='quantity_minus'),
    path('remove_cart/<int:cart_id>', views.remove_cart,name='remove_cart'),
    path('clear_cart/', views.clear_cart,name='clear_cart'),
    path('order_placed/',views.order_placed,name='order_placed'),
    path('order/',views.order,name='order'),
    path('orders/',views.orders,name='orders'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancel_order'),

    path('checkout/', views.checkout,name="checkout"),
    path('search/', views.search,name="search"),

    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path('tracker/', views.tracker,name="tracker"),
]