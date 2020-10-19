from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_id = models.BigAutoField(primary_key = True)
    avatar = models.TextField(null = True)
    real_name = models.TextField()
    age = models.IntegerField(null = True)
    sex = models.IntegerField(null = True)
    certificationType = models.IntegerField(null = True)
    certificationNumber = models.BigIntegerField(null = True)
    address = models.TextField()
    username = models.TextField()
    password = models.TextField()
    telephone = models.TextField()
    class Meta:
        db_table = 'UserInfo'

    def __str__(self):
        return self.username

class UserAccountType(models.Model):
    serial_id = models.BigAutoField(primary_key = True)
    user_id = models.ForeignKey(UserInfo, on_delete = models.CASCADE)
    payment_type = models.TextField()
    account_id = models.TextField()
    priority = models.IntegerField(default = 0)
    class Meta:
        db_table = "UserAccountType"

class Entry(models.Model):
    entry_id = models.BigAutoField(primary_key = True)
    name = models.TextField()
    author = models.TextField(null = True)
    price = models.FloatField()
    original_price = models.FloatField(null = True)
    category = models.TextField(null = True)
    description = models.TextField(null = True)
    customer_inventory = models.IntegerField()
    seller_inventory = models.IntegerField()
    status = models.IntegerField(default = 1)
    seller_id = models.BigIntegerField()
    class Meta:
        db_table = "Entry"

class EntryImage(models.Model):
    entry_id = models.ForeignKey(Entry, on_delete = models.CASCADE)
    image_id = models.IntegerField()
    image = models.TextField()
    class Meta:
        unique_together = ("entry_id", "image_id")
        db_table = "EntryImage"

class EntryComment(models.Model):
    entry_id = models.ForeignKey(Entry, on_delete = models.CASCADE)
    entry_comment_id = models.IntegerField()
    entry_comment = models.TextField()
    comment_time = models.DateTimeField()
    entry_feedback = models.TextField()
    class Meta:
        unique_together = ("entry_id", "entry_comment_id")
        db_table = "EntryComment"

class OrderInfo(models.Model):
    order_id = models.BigAutoField(primary_key = True)
    serial = models.BigIntegerField()
    customer_id = models.BigIntegerField()
    order_time = models.DateTimeField()
    postageFee = models.FloatField()
    paymentType = models.IntegerField()
    class Meta:
        db_table = "OrderInfo"

class OrderDetail(models.Model):
    order_id = models.ForeignKey(OrderInfo, on_delete = models.CASCADE)
    entry_id = models.BigIntegerField()
    number = models.IntegerField()
    seller_id = models.BigIntegerField()
    deliver_time = models.DateTimeField(null = True)
    postageFee = models.FloatField()
    status = models.IntegerField()
    receiveType = models.IntegerField()
    class Meta:
        db_table = "OrderDetail"

class AfterSale(models.Model):
    order_id = models.ForeignKey(OrderInfo, on_delete = models.CASCADE)
    aftersale_post = models.TextField()
    post_time = models.DateTimeField()
    aftersale_feedback = models.TextField(null = True)
    feedback_time = models.DateTimeField(null = True)







