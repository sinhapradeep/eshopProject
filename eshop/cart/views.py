from django.shortcuts import render, redirect
from cart.models.product import Product
from cart.models.category import Category
from cart.models.order import Order
from django.views import View
from .form import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm




class Index(View):
        def post(self, request):
             product = request.POST.get('product')
             remove = request.POST.get('remove')
             cart = request.session.get('cart')
             if cart:
                 quantity = cart.get(product)
                 print(quantity)
                 if quantity:
                     if remove:
                         if quantity <= 1:
                             cart.pop(product)
                         else:
                             cart[product] = quantity - 1
                     else:
                         cart[product] = quantity + 1
                 else:
                     cart[product] = 1
             else:
                 cart = {}
                 cart[product] = 1
             request.session['cart'] = cart
             print("cart", request.session['cart'])
             return redirect("/")


        def get(self, request):
            cart = request.session.get('cart')
            print(cart)
            if not cart:
                request.session['cart'] = {}

            product = None
            categories = Category.get_all_categories()
            #print(request.GET)
            categoryID = request.GET.get('category')
            print(categoryID)
            if categoryID:
                products = Product.get_all_products_by_catgegoryid(categoryID)
            else:
                products = Product.get_all_products()

            data = {}
            data['products'] = products
            data['categories'] = categories

            print('You are :', request.session.get('email'))
            return render(request, 'index.html', data )

class Cart(View):
        def get(self, request):
            ids = list(request.session.get('cart').keys())
            print(ids)
            products = Product.get_products_by_ids(ids)
            print(products)
            return render(request, 'cart.html', {'products': products})

class Orderview(View):
    def get(self, request):
        customer = request.session.get('email')
        orders = Order.get_orders_by_customer( customer)
        print(orders)
        return render(request, 'order.html', {'orders': orders})

class Checkout(View):
        def post(self, request):
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            cart = request.session.get('cart')
            products = Product.get_products_by_ids(list(cart.keys()))

            for product in products:
                order = Order(customer = request.session.get('email'),
                              product = product ,
                              price = product.price ,
                              address = address ,
                              phone = phone ,
                              quantity = cart.get(str(product.id)))
                order.save()

            request.session['cart'] = {}

            return redirect('cart')


def sign_up(request):
      if request.method == 'POST':
            fm = SignUpForm(request.POST)
            # fm = UserCreationForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Account  has been created successfully!!")
      else:
                fm = SignUpForm()
               # fm = UserCreationForm()
      return render(request, 'sign_up.html', {'form': fm})

def ul(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "login successfully!!")
                    request.session['user_id'] = user.id
                    request.session['email'] = user.email
                    print('you 2 are=', request.session.get('email'))
                    print('you 2 are=', request.session.get('user_id'))
                    return HttpResponseRedirect('/user_profile/')
            else:
                messages.error(request, "Invalid Login")
                return redirect('/ul')
        else:
            fm = AuthenticationForm()
            return render(request, 'ul.html', {'form': fm})
    else:
        return HttpResponseRedirect('/user_profile/')

def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')

def user_profile(request):
    categoryID = request.POST.get('category')
    print(categoryID)
    return render(request, 'profile.html', {'name': request.user})

def about(request):

    return render(request, 'about.html')


def test(request):

    return render(request, 'test.html')