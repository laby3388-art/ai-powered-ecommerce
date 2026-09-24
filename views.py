import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Product, Category, CartItem, Order, OrderItem
from .recommendations import recommendations

@ensure_csrf_cookie
def home(request):
    products=Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')
    query=request.GET.get('q','').strip(); category=request.GET.get('category','')
    if query: products=products.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(category__name__icontains=query))
    if category: products=products.filter(category__slug=category)
    picks=recommendations(request.user)
    return render(request,'shop/home.html',{'products':products,'categories':Category.objects.all(),'query':query,'category':category,'picks':picks})

def signup(request):
    error=''
    if request.method=='POST':
        username=request.POST.get('username','').strip(); password=request.POST.get('password','')
        if len(username)<3 or len(password)<8: error='Use a username (3+ characters) and password (8+ characters).'
        elif User.objects.filter(username=username).exists(): error='That username is already in use.'
        else:
            user=User.objects.create_user(username=username,password=password); login(request,user); return redirect('home')
    return render(request,'shop/auth.html',{'mode':'Create account','error':error})

def signin(request):
    form=AuthenticationForm(request, data=request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.get_user()); return redirect('home')
    return render(request,'shop/auth.html',{'mode':'Sign in','form':form,'error':'Check your username and password.' if request.method=='POST' else ''})

def signout(request):
    if request.method=='POST': logout(request)
    return redirect('home')

@login_required
def cart(request):
    rows=CartItem.objects.filter(user=request.user).select_related('product','product__category')
    return render(request,'shop/cart.html',{'rows':rows,'total':sum((x.product.price*x.quantity for x in rows),Decimal('0.00'))})

def payload(request):
    if request.content_type == 'application/json':
        try: return json.loads(request.body or '{}')
        except (json.JSONDecodeError, UnicodeDecodeError): return None
    return request.POST

@login_required
@require_POST
def cart_add(request, product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True)
    data=payload(request)
    if data is None: return HttpResponseBadRequest('Invalid JSON')
    try: quantity=max(1,min(int(data.get('quantity',1)),product.stock))
    except (TypeError,ValueError): return HttpResponseBadRequest('Quantity must be a number')
    if product.stock<1: return JsonResponse({'error':'Out of stock'},status=400)
    item,_=CartItem.objects.get_or_create(user=request.user,product=product)
    item.quantity=min(product.stock,item.quantity+quantity); item.save()
    return JsonResponse({'ok':True,'quantity':item.quantity})

@login_required
@require_POST
def cart_update(request, item_id):
    item=get_object_or_404(CartItem,id=item_id,user=request.user); data=payload(request)
    if data is None: return HttpResponseBadRequest('Invalid JSON')
    try: quantity=int(data.get('quantity',1))
    except (TypeError,ValueError): return HttpResponseBadRequest('Quantity must be a number')
    if quantity<1:
        item.delete()
        return redirect('cart') if request.content_type != 'application/json' else JsonResponse({'ok':True,'removed':True})
    item.quantity=min(quantity,item.product.stock); item.save()
    return redirect('cart') if request.content_type != 'application/json' else JsonResponse({'ok':True,'quantity':item.quantity})

@login_required
@require_POST
def checkout(request):
    with transaction.atomic():
        items=list(CartItem.objects.filter(user=request.user).select_related('product').select_for_update())
        if not items: messages.error(request,'Your cart is empty.'); return redirect('cart')
        if any(i.product.stock<i.quantity for i in items): messages.error(request,'Stock changed. Please review your cart.'); return redirect('cart')
        total=sum((i.product.price*i.quantity for i in items),Decimal('0.00'))
        order=Order.objects.create(user=request.user,total=total)
        for i in items:
            product=Product.objects.select_for_update().get(pk=i.product_id)
            if product.stock < i.quantity: messages.error(request,'Stock changed. Please review your cart.'); return redirect('cart')
            product.stock-=i.quantity; product.save(update_fields=['stock'])
            OrderItem.objects.create(order=order,product=product,product_name=product.name,unit_price=product.price,quantity=i.quantity)
        CartItem.objects.filter(user=request.user).delete()
    messages.success(request,f'Order #{order.id} placed successfully.')
    return redirect('orders')

@login_required
def orders(request): return render(request,'shop/orders.html',{'orders':Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')})

def api_recommendations(request):
    return JsonResponse({'recommendations':[{'id':x['product'].id,'name':x['product'].name,'reason':x['reason']} for x in recommendations(request.user)]})

