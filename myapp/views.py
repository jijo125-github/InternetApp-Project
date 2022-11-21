from datetime import datetime
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, RegisterForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("myapp:login")
        else:
            print('form invalid')
    else:
        form = RegisterForm()
    return render(request=request, template_name="myapp/register.html", context={"register_form": form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                cur_datetime = datetime.now()
                request.session['last_login'] = str(cur_datetime)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:orders'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:login'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'myapp/password_reset.html'
    email_template_name = 'myapp/password_reset_email.html'
    subject_template_name = 'myapp/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('myapp:login')


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    msg = ""
    last_login = "your logged out"
    # print(request.user)
    if request.session.get('last_login', False):
        last_login = datetime.strptime(request.session.get('last_login').split(".")[0], '%Y-%m-%d %H:%M:%S')
        # print(last_login, type(last_login))
        # sleep(2)
        # print(datetime.now(), type(datetime.now()))
        time = datetime.now() - last_login
        if time.total_seconds() > 3600:
            msg = "Your last login was more than one hour ago"
            logout(request)
        # last_login = request.session.get('last_login')
        # login_flag = True
    # else:
    #     last_login = "Your last login was more than one hour ago"
    #     login_flag = False
    context = {
        'cat_list': cat_list,
        'last_login': last_login,
        'user': request.user,
        'msg': msg
    }
    return render(request, 'myapp/index.html', context=context)


def about(request):
    if 'about_visits' in request.COOKIES:
        count_visited = int(request.COOKIES['about_visits'])
        count_visited += 1
    else:
        count_visited = 1
    response = render(request, 'myapp/about.html', {'no_of_times_visited': count_visited})
    response.set_cookie('about_visits', count_visited, max_age=300)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    # return render(request, 'myapp/detail0.html', {'category': category, 'products': products})
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


@login_required
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product']
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                product = Product.objects.get(name=product_name)
                product.stock = product.stock - order.num_units
                product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order !!!'
                return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


@login_required
def productdetail(request, prod_id):
    try:
        msg = ''
        product = Product.objects.get(id=prod_id)
        # product = get_object_or_404(Product, pk=prod_id)
        if request.method == 'GET':
            form = InterestForm()
        elif request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                interested = form.cleaned_data['interested']
                print("Interested: ", interested)
                if int(interested) == 1:
                    product.interested += 1
                    product.save()
                    print('form is valid')
                    return redirect(reverse('myapp:index'))
        # else:
        #     form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'msg': msg, 'product': product})
    except Product.DoesNotExist:
        msg = 'The requested product does not exist. Please provide correct product id !!!'
        return render(request, 'myapp/productdetail.html', {'msg': msg})


def myorders(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return redirect('myapp:login')
        client = Client.objects.get(username=user.username)
        orders = Order.objects.filter(client=client)
        distinct_orders = []
        for order in orders:
            print(order.product.name)
            if order.product.name not in distinct_orders:
                distinct_orders.append(order.product.name)
        msg = f'Orders placed by {client} :-'
        if orders.count() == 0:
            msg = f'{client} has not placed any orders'
        return render(request, 'myapp/myorders.html', {'orders': distinct_orders, 'msg': msg})
    except Client.DoesNotExist:
        msg = 'You are not a registered client'
        return render(request, 'myapp/myorders.html', {'msg': msg})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(profile_form)
        print(request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('myapp:users-profile')
        else:
            print("invalid")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'myapp/profile.html', {'user_form': user_form, 'profile_form': profile_form})
