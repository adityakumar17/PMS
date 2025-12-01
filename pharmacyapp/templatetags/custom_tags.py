from django import template
from pharmacyapp.models import *
from pharmacyapp.views import breaklist
register = template.Library()


@register.filter(name="mystrip")
def mystrip(data):
    data = data[1:-1]
    return data

@register.simple_tag
def pendingbook(data, data2):
    new = Medicine.objects.filter(status='New')
    return new

@register.filter(name='findreportyear')
def findreportyear(year):
    data = History.objects.filter(created__year=year)
    total = 0
    for history_obj in data:
        medicine = history_obj.medicine
        if medicine:
            total += int(medicine.price)
    return total

@register.filter(name='findreportmonth')
def findreportmonth(month):
    data = History.objects.filter(created__month=month)
    total = 0
    for history_obj in data:
        medicine = history_obj.medicine
        if medicine:
            total += int(medicine.price)
    return total

@register.filter(name='findmonth')
def findmonth(month):
    li = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return li[month-1]

@register.filter(name='productname')
def productname(data):
    product = Medicine.objects.get(id=data)
    return product.medicinename

@register.filter(name='productprice')
def productprice(data):
    product = Medicine.objects.get(id=data)
    return product.price

@register.simple_tag
def producttotalprice(data, user, order=None):
    product = Medicine.objects.get(id=data)
    if order:
        datao = Order.objects.get(id=order)
        qtyli = breaklist(datao.quantity)
        proli = breaklist(datao.productid)
    else:
        cart = Cart.objects.get(user__user=user)
        qtyli = breaklist(cart.quantity)
        proli = breaklist(cart.productid)
    pindex = proli.index(data)
    qqty = int(qtyli[pindex])
    return qqty*int(product.price)

# @register.simple_tag
# def ordertotalprice(data, obj):
#     product = Medicine.objects.get(id=data)
#     order = Order.objects.get(id=obj)
#     qtyli = breaklist(order.quantity)
#     print(order.productid)
#     proli = breaklist(order.productid)
#     pindex = proli.index(data)
#     qqty = int(qtyli[pindex])
#     return format(qqty*product.price, '.2f')

@register.simple_tag
def productqty(data, user, order=None):
    product = Medicine.objects.get(id=int(data))
    if order:
        datao = Order.objects.get(id=order)
        qtyli = breaklist(datao.quantity)
        proli = breaklist(datao.productid)
    else:
        cart = Cart.objects.get(user__user=user)
        qtyli = breaklist(cart.quantity)
        proli = breaklist(cart.productid)
    pindex = proli.index(int(data))
    qqty = int(qtyli[pindex])
    return qqty

@register.simple_tag
def totalpricehitsory(qty, price):
    return int(qty) * int(price)

@register.filter(name='totalpricea')
def totalpricea(s, pid=None):
    if pid:
        invoice = Medicine.objects.get(id=pid)
        cart = Order.objects.get(id=invoice.invoice.id)
    else:
        cart = Order.objects.filter().first()
    if cart:
        qty = breaklist(cart.quantity)
        pro = breaklist(cart.productid)
        total = 0
        for i in pro:
            product = Medicine.objects.get(id=i)
            myindex = pro.index(i)
            qtyid = qty[myindex]
            total = total + (int(product.price) * int(qtyid))
        return total
    return 0
