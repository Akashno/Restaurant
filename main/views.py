import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect

from main.decorators import user_view, admin_view, unauthenticated_view
from main.forms import CreateUserForm
from main.models import Products, Cart, Orders, Payment, Table, Reservation, Notifications


@login_required(login_url='account_login')
@user_view
def index(request):
    # tables =Table.objects.all()
    # for table in tables:
    #     table.reserved =False
    #     table.save()

    context = {}
    return render(request, 'index.html', context)


@login_required(login_url='login_page')
@user_view
def products(request):
    if Cart.objects.count() > 0:
        found = True
    else:
        found = False
    cart = Cart.objects.filter(user=request.user)
    products = Products.objects.all()

    product_count = Cart.objects.aggregate(Sum('count'))
    product_total = Cart.objects.aggregate(Sum('total'))

    context = {"found": found, "products": products, "cart": cart, 'pc': product_count['count__sum'],
               'pt': product_total['total__sum']}
    return render(request, 'products.html', context)


@login_required(login_url='login_page')
@user_view
def add_cart(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == "POST":
        if Cart.objects.filter(product=product).exists():

            item = Cart.objects.get(product=product)
            item.update_count()
            item.get_total()
            item.save()
            return redirect('products')
        else:
            cart = Cart(user=request.user, product=product)
            cart.get_total()
            cart.save()

            return redirect('products')

    context = {"product": product}
    return render(request, 'add_cart.html', context)


@login_required(login_url='login_page')
@user_view
def delete_cart(request, pk):
    item = Cart.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('products')
    return render(request, 'delete_cart.html', )


@login_required(login_url='login_page')
@user_view
def empty_cart(request):
    Cart.objects.all().delete()
    return redirect('products')


@login_required(login_url='login_page')
@user_view
def add_order(request):
    items = Cart.objects.all()

    for item in items:
        order = Orders(user=item.user, product=item.product, count=item.count, total=item.total)

        order.save()
    messages.success(request, "New Orders Placed Successfully")
    Cart.objects.all().delete()
    return redirect('profile')


@login_required(login_url='login_page')
@user_view
def delete_order(request, pk):
    item = Orders.objects.get(id=pk)
    item.delete()
    messages.info(request, 'Order successfully canceled')
    return redirect('profile')


@login_required(login_url='login_page')
@user_view
def table(request):
    tables = Table.objects.all()
    date = limit_date()

    context = {'tables': tables, 'date': date}
    return render(request, 'table.html', context)


@login_required(login_url='login_page')
@user_view
def add_reservation(request, pk):
    table = Table.objects.get(id=pk)
    reserve = Reservation(user=request.user, table=table, date=request.POST['date'], time=request.POST['time'])
    reserve.save()

    messages.success(request, "Reservation for Table No." + str(pk) + "for" + str(request.POST['date']) + ' at ' + str(
        request.POST['time']) + "was made,please wait for confirmation message ")
    return redirect('profile')


@login_required(login_url='login_page')
@user_view
def profile(request):
    if request.user.is_superuser:
        orders = Orders.objects.all().order_by('-id')
        reservations = Reservation.objects.all().order_by('-id')

    else:
        orders = Orders.objects.filter(user=request.user)
        reservations = Reservation.objects.filter(user=request.user)
        notifications = Notifications.objects.filter(user=request.user)
    context = {"orders": orders, 'reservations': reservations, 'notifications': notifications}

    return render(request, 'profile.html', context)


@login_required(login_url='login_page')
@user_view
def payment(request):
    product_total = Cart.objects.filter(user=request.user).aggregate(Sum('total'))
    if request.method == "POST":
        p = Payment(
            user=request.user,
            acnumber=request.POST.get('acnumber'),
            expirem=request.POST.get('expirem'),
            expirey=request.POST.get('expirey'),
            ccv=request.POST.get('ccv'),
        )
        messages.success(request, "Payment Confirmed ")
        if Payment.objects.filter(user=request.user).exists():
            return redirect('add_order')
        p.save()
        return redirect('add_order')
    context = {"product_total": product_total['total__sum']}
    return render(request, 'payment.html', context)


@unauthenticated_view
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Registration successfull for ' + username)
            return redirect('login_page')

    context = {"form": form}
    return render(request, 'register.html', context)


@unauthenticated_view
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        if user.is_staff:
            return redirect('admin_page')
        else:
            return redirect('index')
        messages.error(request, 'invalid username or password')

    context = {}
    return render(request, 'login.html', context)


def logout_page(request):
    Cart.objects.all().delete()
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@admin_view
def admin_page(request):
    orders = Orders.objects.filter(delivered=False)
    reservations = Reservation.objects.all()

    # do unsubscribe
    context = {'orders': orders, 'reservations': reservations}
    return render(request, 'admin_page.html', context)


@admin_view
def admin_approval(request, pk):
    if request.method == "POST":
        if 'deliver_order' in request.POST:
            order = Orders.objects.get(id=pk)
            order.delivered = True
            order.save()
            messages.success(request, "order delivered")
            notification = Notifications(user=order.user, notification="order for " + str(order.count) + " " + str(
                order.product.name) + " is delivered")
            notification.save()

        elif 'cancel_order' in request.POST:
            order = Orders.objects.get(id=pk)
            notification = Notifications(user=order.user, notification="order for " + str(order.count) + " " + str(
                order.product.name) + " was canceled")
            notification.save()
            order.delete()
            messages.success(request, "order canceled")


        elif 'approve_reservation' in request.POST:
            reservation = Reservation.objects.get(id=pk)

            table = Table.objects.get(id=reservation.table.id)

            table.reserved = True

            table.save()
            notification = Notifications(user=reservation.user,
                                         notification="Reservation for Table number: " + str(table.id) + " Approved")
            messages.success(request, "Reservation approved")
            notification.save()

        elif 'cancel_reservation' in request.POST:
            reservation = Reservation.objects.get(id=pk)
            table = Table.objects.get(id=reservation.table.id)
            table.reserved = False
            table.save()
            reservation.delete()
            notification = Notifications(user=reservation.user, notification="Reservation for Table number: " + str(
                table.id) + " was canceled")
            notification.save()

            messages.success(request, "Reservation canceled")

    return redirect('admin_page')

def aprofile(request):
    return redirect('index')
# tweeks
# make tables unreserved
# tables =Table.objects.all()
# for table in tables:
#     table.reserved =False
#     table.save()

def limit_date():
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    if len(str(month)) > 1:
        pass
    else:
        month = str(month).zfill(2)
    if len(str(day)) > 1:
        pass
    else:
        day = str(day).zfill(2)
    date = str(year) + '-' + str(month) + '-' + str(day)
    return date
