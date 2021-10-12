
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.db.models import Q
from django.utils.decorators import method_decorator


class ShopHomePage(View):
    template_name = 'shop/home.html'
    def get(self, request):
        products = Product.objects.all()
        clothes = Product.objects.filter(category='Clothes')
        electronics = Product.objects.filter(category='Electronics')
        context = {'products':products,'clothes':clothes, 'electronics':electronics}
        return render(request,self.template_name,context)

@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    template_name = 'shop/dashboard.html'
    def get(self, request):
        context = {}
        return render(request,self.template_name,context)


def search(request):
    query = request.GET.get('search')
    query = query.strip()
    query = query.lower()
    # products = Product.objects.filter(Q(product_name = query) | Q(category=query) | Q(sub_category=query))
    prods = Product.objects.values('product_name','category','sub_category')
    prods_name_list  = [i['product_name'] for i in prods]
    prods_category_list  = [i['category'] for i in prods]
    prods_sub_category_list  = [i['sub_category'] for i in prods]

    prod_s =[]
    for i in prods_name_list:
        if i.lower() == query:
            item = Product.objects.get(product_name = i)
            prod_s.append(item)
        else:
            for  j in i.split():
                if j.lower() == query:
                    item = Product.objects.get(product_name = i)
                    prod_s.append(item)
    
    for i in prods_category_list:
            if i.lower() == query:
                item = Product.objects.filter(category = i)
                prod_s.extend(item)

    for i in prods_sub_category_list:
            if i.lower() == query:
                item = Product.objects.filter(sub_category = i)
                prod_s.extend(item)
    
    prod_s = set(prod_s)
    prod_s = list(prod_s)
    products = prod_s
    context = {'products':products, 'query':query}
    return render(request,'shop/search.html', context)


@login_required(redirect_field_name='login',login_url='/login/')
def add_to_cart(request,product_id=None):
    product = Product.objects.get(product_id=product_id)
    user = request.user
    cart = Cart(user=user, product_name=product)
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 

@login_required(redirect_field_name='login',login_url='/login/')
def buy_now(request,product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user
    cart = Cart(user=user, product_name=product)
    cart.save()
    return redirect('checkout')

@login_required(redirect_field_name='login',login_url='/login/')
def mycart(request):
    cart = Cart.objects.filter(user=request.user)
    tot_price = 0
    for product in cart:
        tot_price += product.product_name.price * product.quantity
    context = {'cart':cart,'tot_price':tot_price}
    return render(request,'shop/mycart.html', context)

def quantity_plus(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    cart_prod.quantity += 1
    cart_prod.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 
    # return redirect('mycart')

def quantity_minus(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    if cart_prod.quantity > 1:
        cart_prod.quantity -= 1
        cart_prod.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 
    return redirect('mycart')

def remove_cart(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    cart_prod.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page
    # return redirect('mycart')

def clear_cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

# @login_required(redirect_field_name='login',login_url='/login/')
# def checkout(request):
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = AddressForm()
#     cart = Cart.objects.filter(user=request.user)
#     addresses = Address.objects.filter(user=request.user)
#     tot_price = 0
#     for product in cart:
#         tot_price += product.product_name.price * product.quantity
#     context={'cart':cart,'addresses':addresses, 'tot_price':tot_price, 'form':form}
#     return render(request,'shop/checkout.html',context)
    

class Checkout(View):
    template_name = 'shop/checkout.html'
    def get(self, request):
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = AddressForm()
        cart = Cart.objects.filter(user=request.user)
        addresses = Address.objects.filter(user=request.user)
        tot_price = 0
        for product in cart:
            tot_price += product.product_name.price * product.quantity
        context={'cart':cart,'addresses':addresses, 'tot_price':tot_price, 'form':form}
        return render(request,self.template_name,context)
    

def productview(request,product_id=None):
    product = Product.objects.get(product_id=product_id)
    context ={'product':product}
    return render(request,'shop/productview.html',context)

def address(request):
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses':addresses}
    return render(request,'shop/address.html',context)

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone_number']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip = form.cleaned_data['zip']
            
            fm = Address(user=request.user, phone_number=phone, address=address, city=city, state=state, zip= zip)
            fm.save()
            messages.success(request,'Your Address Added Successfully')
            return redirect('address')
    else:
        form = AddressForm()
    context = {'form':form}
    return render(request,'shop/add_address.html',context)

def delete_address(request,id=None):
    address = Address.objects.get(pk=id)
    address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

def order_placed(request):
    return render(request,'shop/odered_placed.html')

def order(request):
    cart = Cart.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)[0]
    product_count = len(cart)
    temp = 0
    for i in cart:
        temp += i.product_name.price * i.quantity
    total_price = temp + 70
    order = Order(user=request.user,product_count=product_count,total_amount=total_price,order_date=timezone.now())
    order.save()

    ord_address = Ordered_Address(user=request.user,order=order,address=address.address,phone_number=address.phone_number,city=address.city,state=address.state,zip=address.zip)
    ord_address.save()

    for i in cart:
        product = i.product_name
        quantity = i.quantity
        ord_prod = Ordered_Product(order=order,product=product,quantity=quantity)
        ord_prod.save()

    
    cart.delete()
    # return redirect('order_placed')

    # Request paytm to transfer the amount to your account after payment by user
    # MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
    # param_dict = {
    #     'MID': 'WorldP64425807474247',
    #     'ORDER_ID': str(order.id),
    #     'TXN_AMOUNT': '1',
    #     'CUST_ID': request.user.email,
    #     'INDUSTRY_TYPE_ID': 'Retail',
    #     'WEBSITE': 'WEBSTAGING',
    #     'CHANNEL_ID': 'WEB',
    #     'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
    # }
    # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    # return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return redirect('order_placed')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    return HttpResponse('done')
    
def orders(request):
    orders  = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,'shop/orders.html',context)

def cancel_order(request,id=None):
    order = Order.objects.get(pk=id)
    print(order.status)
    if order.status == 'On The Way' or order.status == 'Delivered':
        messages.warning(request,f'Soory, You Can\'t Cancel This Order Now')
    else:
        messages.success(request,f'Order Cancelled Successfully')
        order.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    return render(request,'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')


def checkout(request):
    return render(request,'shop/checkout.html')