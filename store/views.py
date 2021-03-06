from distutils.log import error
from http.client import HTTPResponse
from itertools import product
from logging import exception
from math import degrees
from turtle import title
from unicodedata import category
from django.shortcuts import render,get_object_or_404,redirect
from store.models import Category,Product,Cart,CartItem,Order,OrderItem,image_product,Contact
from store.forms import SignUpForm
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.http import HttpResponse
# Create your views here.
def index(request,category_slug=None):
    products=None
    category_page=None
    if category_slug!=None:
        category_page=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(category=category_page,available=True)
        
    else :
        products=Product.objects.all().filter(available=True)

    paginator=Paginator(products,3)
    try:
        page=int(request.GET.get('page','1'))
    except :
        page=1
    
    try:
        productperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage=paginator.page(paginator.num_pages)

    filter_district = request.GET.get('filter_district', None)
    if filter_district == "ASC":
        products = Product.objects.all().filter().order_by('price')
    elif  filter_district == "DESC ":
        products = Product.objects.all().filter().order_by('-price')

    imgs=[]
    product_image =[]
    for prod in products:
        img  = image_product.objects.filter(product=prod.id).first()
        # imgs.append(img.image.url)
        product_image.append({'product':prod, 'img':img.image.url})
        
    return render(request,'index.html',{'products':productperPage,'category':category_page,'imgs':imgs,'prod':product_image})

def productPage(request,category_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        images = image_product.objects.filter(product=product)
    except Exception as e:
        raise e
    

    return render(request,'product.html',{'product':product,'images':images})

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

@login_required(login_url='signIn')
def addCart(request,product_id):
    #?????????????????????????????????????????????????????????????????????????????????
     product=Product.objects.get(id=product_id)

     #???????????????????????????????????????????????????
     try:
         cart=Cart.objects.get(cart_id=_cart_id(request))
     except Cart.DoesNotExist:
         cart=Cart.objects.create(cart_id=_cart_id(request))
         cart.save()
    
     try:
        #???????????????????????????????????????
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock :

            #???????????????????????????????????????????????????????????????
            cart_item.quantity+=1
            #??????????????????/???????????????????????????
            cart_item.save()
     except CartItem.DoesNotExist:
         #??????????????????????????????????????????????????????
         #???????????????????????????????????????????????????
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
     return redirect('/')

def cartdetail(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass
    stripe.api_key=settings.SECRET_KEY
    stripe_total=int(total*100)
    description="Payment Online"
    data_key=settings.PUBLIC_KEY

    if request.method=="POST":
        try:
            token=request.POST['stripeToken']
            email=request.POST['stripeEmail']
            name=request.POST['stripeBillingName']
            address=request.POST['stripeBillingAddressLine1']
            city=request.POST['stripeBillingAddressCity']
            postcode=request.POST['stripeShippingAddressZip']
            
            customer=stripe.Customer.create(
                email=email,
                source=token
            )
            charge=stripe.Charge.create(
                amount=stripe_total,
                currency='thb',
                description=description,
                customer=customer.id
            )
            #??????????????????????????????????????????????????????????????????
            order=Order.object.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total,
                email=email,
                token=token
            )
            order.save()

            #????????????????????????????????????????????????????????????
            for item in cart_items :
                order_item=OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order
                )
                order_item.save

                #????????????????????? stock 
                Product.objects.get(id=order_item.product.id)
                product.stock=int(order_item.product.stock-order_item.quantity)
                product.save()
                item.delete()
            return redirect('home')

        except stripe.error.CardError as e :
            return False , e

    return render(request,'cartdetail.html',
    dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))

def removeCart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    #???????????????????????????????????????????????????????????????
    product=get_object_or_404(Product,id=product_id)
    cartItem=CartItem.objects.get(product=product,cart=cart)

    cartItem.delete()
    return redirect('cartdetail')

def signUpView(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            #???????????????????????????????????? User
            form.save()
            #?????????????????? Group Customer
            #????????? username ????????????????????????????????????????????????
            username=form.cleaned_data.get('username')
            #??????????????????????????? user ????????????????????????????????????
            signUpUser=User.objects.get(username=username)
            #????????? Group
            customer_group=Group.objects.get(name="Customer")
            customer_group.user_set.add(signUpUser)
    else :
        form=SignUpForm()
    return render(request,"signup.html",{'form':form})

def signInView(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                return redirect('signUp')
    else :
        form=AuthenticationForm()
    return render(request,'signIn.html',{'form':form})

def signOutView(request):
    logout(request)
    return redirect('signIn')

def search(request):
    search_name = request.GET['title']
    product_name=Product.objects.filter(name__contains=search_name)

    product_image =[]
    for prod in product_name:
        img  = image_product.objects.filter(product=prod.id).first()
        # imgs.append(img.image.url)
        product_image.append({'product':prod, 'img':img.image.url})

    return render(request,'search.html',{'product':product_image, 'image':product_image})

def contact(request):
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        comment=request.POST.get('comment')

        contact.first_name=name
        contact.last_name=lastname
        contact.email=email
        contact.comment=comment
        contact.save()
        
        return HttpResponse()

    return render(request,'contact.html')