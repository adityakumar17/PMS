from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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

class Pharmacist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    last = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    companyname = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.companyname

class Medicine(models.Model):
    companyname = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    medicinename = models.CharField(max_length=200, null=True, blank=True)
    batchnumber = models.CharField(max_length=200, null=True, blank=True)
    mgfdate = models.CharField(max_length=200, null=True, blank=True)
    expirydate = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    qty = models.CharField(max_length=200, null=True, blank=True, default="20")
    price = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicinename

    def soldqty(self):
        return int(self.qty) - int(self.quantity)

    def remaining(self):
        price = int(self.qty) - int(self.quantity)
        return int(self.quantity) - price


ORDERSTATUS = (
(1, "Dispatch"), (2, "Shipped"), (3, "On the way"), (4, "nearest to location"), (5, "Delivered"), (6, "Cancel"),
(7, "Return"), (8, "Refund"), (9, "Exchange"))
class Order(models.Model):
    user = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    orderid = models.CharField(max_length=100, null=True, blank=True)
    productid = models.TextField(max_length=100, null=True, blank=True)
    quantity = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=ORDERSTATUS, default=1)
    custmobile = models.CharField(max_length=200, null=True, blank=True)
    custname = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    payment = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


    def totalprice(self):
        qtyvalues = breaklist(self.quantity)
        prokey = breaklist(self.productid)
        total = 0
        res = dict(map(lambda i, j: (i, j), prokey, qtyvalues))
        for i, j in res.items():
            medicine = Medicine.objects.get(id=i)
            total += (int(medicine.price) * int(j))
        return total

class Cart(models.Model):
    user = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True, blank=True)
    productid = models.TextField(null=True, blank=True)
    quantity = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.user.username

class History(models.Model):
    user = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.user.username



