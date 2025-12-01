import json
from random import randint
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import *

from .models import *
from django.db.models import Sum, F, Value, IntegerField
from django.db.models.functions import Coalesce, Cast


# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url='/admin_login/')
def dashboard(request):
    today = datetime.date.today()
    todaydata = Order.objects.filter(updated__date=today,)
    todaydata_amount = 0
    for i in todaydata:
        if i.totalprice():
            todaydata_amount += int(i.totalprice())

    last7 = datetime.date.today() - datetime.timedelta(days=7)
    last7data = Order.objects.filter(updated__date__gte=last7)
    last7data_amount = 0
    for i in last7data:
        if i.totalprice():
            last7data_amount += int(i.totalprice())

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdaydata = Order.objects.filter(updated__date=yesterday)
    yesterdaydata_amount = 0
    for i in yesterdaydata:
        if i.totalprice():
            yesterdaydata_amount += int(i.totalprice())

    total = Pharmacist.objects.all()

    order = Order.objects.filter()
    total_amount = 0
    for i in order:
        if i.totalprice():
            total_amount += int(i.totalprice())
    all = Company.objects.all()
    medicine = Medicine.objects.all()
    return render(request, "admin_dashboard.html",locals())

@login_required(login_url='/pharmacist_login/')
def user_dashboard(request):
    today = datetime.date.today()
    todaydata = Order.objects.filter(updated__date=today, user__user=request.user)
    todaydata_amount = 0
    for i in todaydata:
        if i.totalprice():
            todaydata_amount += int(i.totalprice())

    last7 = datetime.date.today() - datetime.timedelta(days=7)
    last7data = Order.objects.filter(updated__date__gte=last7, user__user=request.user)
    last7data_amount = 0
    for i in last7data:
        if i.totalprice():
            last7data_amount += int(i.totalprice())

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdaydata = Order.objects.filter(updated__date=yesterday, user__user=request.user)
    yesterdaydata_amount = 0
    for i in yesterdaydata:
        if i.totalprice():
            yesterdaydata_amount += int(i.totalprice())

    order = Order.objects.filter(user__user=request.user)
    total_amount = 0
    for i in order:
        if i.totalprice():
            total_amount += int(i.totalprice())

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))

    return render(request, "user_dashboard.html", locals())

@login_required(login_url='/pharmacist_login/')
def user_inventory(request):
    data = Medicine.objects.all()
    d = {'data': data}

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, "user_inventory.html", locals())

@login_required(login_url='/admin_login/')
def admin_medicine_inventory(request):
    data = Medicine.objects.all()
    d = {'data': data}
    return render(request, "admin_medicine_inventory.html", d)

def admin_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                messages.success(request, "Invalid User")
                return redirect('admin_login')
    return render(request, "login.html")

@login_required(login_url='/admin_login/')
def logout_admin(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('admin_login')\

@login_required(login_url='/pharmacist_login/')
def logout_user(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('pharmacist_login')

@login_required(login_url='/admin_login/')
def admin_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

@login_required(login_url='/pharmacist_login/')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        uname = request.POST['username']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email, username=uname)
        Pharmacist.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Pharmacist.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/pharmacist_login/')
def user_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')
    return render(request, 'user_change_password.html')

@login_required(login_url='/admin_login/')
def add_company(request, pid=None):
    company = None
    if pid:
        company = Company.objects.get(id=pid)
    if request.method == "POST":
        company = CompanyForm(request.POST, request.FILES, instance=company)
        if company.is_valid():
            new_company = company.save()
            new_company.save()
        if pid:
            messages.success(request, "Update Company Successful")
            return redirect('view_company')
        else:
            messages.success(request, "Add Company Successful")
            return redirect('view_company')
    return render(request, 'add_company.html', locals())

@login_required(login_url='/admin_login/')
def view_company(request):
    data = Company.objects.all()
    d = {'data': data}
    return render(request, "view_company.html", d)

@login_required(login_url='/admin_login/')
def delete_company(request, pid):
    data = Company.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_company')

@login_required(login_url='/admin_login/')
def add_medicine(request, pid=None):
    medicine = None
    if pid:
        medicine = Medicine.objects.get(id=pid)
    if request.method == "POST":
        medicine = MedicineForm(request.POST, request.FILES, instance=medicine)
        if medicine.is_valid():
            new_medicine = medicine.save()
            new_medicine.qty = request.POST['quantity']
            new_medicine.save()
        if pid:
            messages.success(request, "Update Medicine Successful")
            return redirect('view_medicine')
        else:
            messages.success(request, "Add Medicine Successful")
            return redirect('view_medicine')
    mycompany = Company.objects.all()
    return render(request, 'add_medicine.html', locals())

@login_required(login_url='/admin_login/')
def view_medicine(request):
    data = Medicine.objects.all()
    d = {'data': data}
    return render(request, "view_medicine.html", d)

@login_required(login_url='/admin_login/')
def delete_medicine(request, pid):
    data = Medicine.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_medicine')

@login_required(login_url='/admin_login/')
def add_pharmacist(request, pid=None):
    user = None
    pharmacist = None
    if pid:
        user = User.objects.get(id=pid)
        pharmacist = Pharmacist.objects.get(user=user)
    if request.method == "POST":
        form = PharmacistForm(request.POST, request.FILES, instance=pharmacist)
        if form.is_valid():
            new_pharmacist = form.save()
            if pid:
                new_user = User.objects.filter(id=pid).update(first_name=request.POST['firstname'], username=request.POST['username'])
            else:
                new_user = User.objects.create_user(first_name=request.POST['firstname'], username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                new_pharmacist.user = new_user
                new_pharmacist.save()

        messages.success(request, "Pharmacist saved successful")
        return redirect('view_pharmacist')
    return render(request, 'add_pharmacist.html', locals())

@login_required(login_url='/admin_login/')
def view_pharmacist(request):
    data = Pharmacist.objects.all()
    d = {'data': data}
    return render(request, "view_pharmacist.html", d)

@login_required(login_url='/admin_login/')
def delete_pharmacist(request, pid):
    data = Pharmacist.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_pharmacist')

def pharmacist_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('pharmacist_login')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('user_dashboard')
        else:
            messages.success(request, "Invalid User")
            return redirect('pharmacist_login')
    return render(request, "pharmacist_login.html")


@login_required(login_url='/pharmacist_login/')
def user_search_medicine(request):
    data = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data = Medicine.objects.filter(medicinename__icontains=fromdate).exclude(quantity='0')

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, "user_search_medicine.html", locals())


def changeinInt(li):
    myli = []
    for i in li:
        myli.append(int(i))
    return myli


def breaklist(mystr):
    pid = mystr
    pid2 = pid[1:-1]

    if pid2 == "":
        return []
    else:
        pid3 = pid2.split(',')
        pid3 = changeinInt(pid3)
        return pid3


def myexistingid(li, pid, quantity, qty):
    if pid in li:
        pindex = li.index(pid)
        qqty = int(quantity[pindex]) + int(qty)
        quantity[pindex] = qqty
        return quantity, li
    else:
        quantity.append(qty)
        li.append(pid)
        return quantity, li


# def mycart(request):
#     productid = []
#     try:
#         cart = Cart.objects.get(user__user=request.user)
#         myli = breaklist(cart.productid)
#         productid = myli
#     except:
#         productid = []
#     lengthpro = len(productid)
#     return render(request, 'mycart.html', locals())

def add_cart(request, pid):
    qty = int(request.GET.get('qty'))
    pro = Medicine.objects.get(id=pid)
    if int(pro.quantity) < qty:
        messages.success(request, "Minimum Quantity is "+pro.quantity)
        return redirect('/user_search_medicine/')
    else:
        pro.quantity = int(pro.quantity) - qty
        pro.save()
    try:
        cart = Cart.objects.get(user__user=request.user)

        myli = breaklist(cart.productid)
        myliqty = breaklist(cart.quantity)
        myqty, myli = myexistingid(myli, pid, myliqty, qty)

        cart.productid = myli
        cart.quantity = myqty
        cart.save()
    except:
        pidli = [pid]
        myuser = Pharmacist.objects.get(user=request.user)
        Cart.objects.create(user=myuser, productid=pidli, quantity=[qty])
    messages.success(request, "Added a item in cart.")
    return redirect('user_cart')

def view_cart(request):
    data = Cart.objects.all()
    d = {'data': data}
    return render(request, "manage_cart.html", d)

def deletecart(request, pid):
    cart = Cart.objects.get(user__user=request.user)
    qtyli = breaklist(cart.quantity)
    proli = breaklist(cart.productid)
    pindex = proli.index(pid)
    main_qty = qtyli[pindex]
    qtyli.pop(pindex)
    proli.pop(pindex)
    cart.quantity = qtyli
    cart.productid = proli
    cart.save()
    medicine = Medicine.objects.get(id=pid)
    medicine.quantity =  int(medicine.quantity) + int(main_qty)
    medicine.save()
    messages.success(request, "Remove a item from cart.")
    return redirect('user_cart')

@login_required(login_url='/admin_login/')
def admin_stock_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        data = Medicine.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "admin_stock_report.html", locals())

@login_required(login_url='/admin_login/')
def user_sales_report(request):
    data = None
    data2 = None
    productid = []
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        data = History.objects.filter(created__date__gte=fromdate, created__date__lte=todate, user__user=request.user)\
            .values('medicine__id', 'medicine__medicinename', 'medicine__price')\
            .distinct()\
            .annotate(num_order=Count('medicine__id'))
        data2 = True

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, "user_sales_report.html", locals())

@login_required(login_url='/admin_login/')
def admin_pharmacist_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        pharmacist = request.POST['pharmacist']
        data = History.objects.filter(created__date__gte=fromdate, created__date__lte=todate, user__id=pharmacist) \
            .values('medicine__id', 'medicine__medicinename', 'medicine__price') \
            .distinct() \
            .annotate(num_order=Count('medicine__id'))
        data2 = True
    pharmacist = Pharmacist.objects.all()
    return render(request, "admin_pharmacist_report.html", locals())

@login_required(login_url='/pharmacist_login/')
def user_invoice(request):
    data = None
    data2 = None
    productid = []
    if request.method == "POST":
        fromdate= request.POST['fromdate']
        data2 = True
        try:
            data = Order.objects.get(Q(orderid=fromdate,user__user=request.user))

            try:
                myli = breaklist(data.productid)
                productid = myli
            except:
                productid = []
        except:
            data= None

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, "user_invoice.html", locals())

@login_required(login_url='/admin_login/')
def admin_invoice(request):
    data = None
    data2 = None
    productid = []
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        try:
            data = Order.objects.get(Q(orderid=fromdate))

            try:
                myli = breaklist(data.productid)
                productid = myli
            except:
                productid = []
        except:
            data = None
    return render(request, "admin_invoice.html", locals())

def random_with_N_digits(n):
    range_start = 6**(n-1)
    range_end = (6**n)-1
    return randint(range_start, range_end)

@login_required(login_url='/admin_login/')
def user_cart(request):
    productid = []
    try:
        cart = Cart.objects.get(user__user=request.user)
        myli = breaklist(cart.productid)
        productid = myli

    except:
        productid = []
    lengthpro = len(productid)
    if request.method == "POST":
        re = request.POST
        user = Pharmacist.objects.get(user=request.user)
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(orderid=random_with_N_digits(10), productid=cart.productid,
            quantity=cart.quantity, user=user, custmobile=re['custmobile'], payment=re['payment'], custname=re['custname'])

        cart.productid = []
        cart.quantity = []
        cart.save()
        productid = []
        try:
            proli = breaklist(order.productid)
            productid = proli
        except:
            productid = []
        for i in productid:
            medicine = Medicine.objects.get(id=i)
            qty = breaklist(order.quantity)
            proindex = productid.index(i)
            qtyli = qty[proindex]
            for j in range(qtyli):
                history = History.objects.create(medicine=medicine, user=user)
        messages.success(request, "Invoice Created Successful Billing Number is   " + str(order.orderid))
        return redirect('user_cart')

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, 'user_cart.html', locals())

def admin_sales_report(request):
    data = None
    fromdate = None
    todate = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        req = request.POST.get('reqtype')
        print(fromdate)
        mont1 = int(fromdate.split('-')[1])
        mont2 = int(todate.split('-')[1])
        yer1 = int(fromdate.split('-')[0])
        yer2 = int(todate.split('-')[0])
        monthli = [i for i in range(mont1, mont2+1)]
        yearli = [i for i in range(yer1, yer2+1)]
    return render(request, "admin_sales_report.html",locals())

def order(request):
    data = Order.objects.filter()
    action = request.GET.get('action')
    if action == "Today":
        today = datetime.date.today()
        data = data.filter(updated__date=today)
    if action == "Yesterday":
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = data.filter(updated__date=yesterday)
    if action == "Last 7 days":
        last7 = datetime.date.today() - datetime.timedelta(days=7)
        data = data.filter(updated__date__gte=last7)
    d = {'data': data}
    return render(request, "day_view.html", d)

@login_required(login_url='/admin_login/')
def delete_order(request, pid):
    data = Order.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('order')


@login_required(login_url='/pharmacist_login/')
def user_order(request):
    data = Order.objects.filter(user__user=request.user)
    action = request.GET.get('action')
    if action == "Today":
        today = datetime.date.today()
        data = data.filter(updated__date=today)
    if action == "Yesterday":
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = data.filter(updated__date=yesterday)
    if action == "Last 7 days":
        last7 = datetime.date.today() - datetime.timedelta(days=7)
        data = data.filter(updated__date__gte=last7)
    d = {'data': data}

    cart_items = Cart.objects.filter(user__user=request.user)
    item_count = 0
    for cart_item in cart_items:
        item_count += len(breaklist(cart_item.productid))
    return render(request, "user_day_view.html", locals())

@login_required(login_url='/pharmacist_login/')
def user_delete_order(request, pid):
    data = Order.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('user_order')