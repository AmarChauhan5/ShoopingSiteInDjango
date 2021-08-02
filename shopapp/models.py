from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICES = (
   ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
   ("Andhra Pradesh","Andhra Pradesh"),
   ("Arunachal Pradesh","Arunachal Pradesh"),
   ("Assam","Assam"),
   ("Bihar","Bihar"),
   ("Chhattisgarh","Chhattisgarh"),
   ("Chandigarh","Chandigarh"),
   ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
   ("Daman and Diu","Daman and Diu"),
   ("Delhi","Delhi"),
   ("Goa","Goa"),
   ("Gujarat","Gujarat"),
   ("Haryana","Haryana"),
   ("Himachal Pradesh","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("Maharashtra","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street = models.CharField(max_length=150)
    village = models.CharField(max_length=150)
    district = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES,max_length=50,default='Maharashtra')
    pin_code = models.IntegerField()
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return str(self.id)

CATAGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    catagory = models.CharField(choices=CATAGORY_CHOICES,max_length=10)
    product_image = models.ImageField(upload_to='productimage')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_amount(self):
        return self.quantity*self.product.selling_price

    def __str__(self):
        return str(self.id)
STATUS_CHOICE = (
    ('P','Pending'),
    ('A','Accepted'),
    ('PD','Packed'),
    ('OTW','On The Way'),
    ('D','Delivered'),
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE,default='P',max_length=15)

    def total_amount(self):
        return self.quantity*self.product.selling_price

    def __str__(self):
        return str(self.id)
