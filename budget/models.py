from django.db import models
from django.contrib.auth.models import User


# Create your models here.





class Category(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank =True)
    TYPE = (
            ('Income', 'Income'),
            ('Expense', 'Expense'),)
    category_feild =  models.CharField(max_length = 100,unique = False)
    income_or_expense = models.CharField(default =" ",max_length=200, choices=TYPE)

    def __str__(self):
        return self.category_feild



class Budget(models.Model):
    
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)
    budget_amt = models.FloatField(default= 0)
    comments = models.CharField(max_length = 140,default="")

    def __str__(self):

        return self.category.category_feild +' - ' + str(self.date.strftime('%b %Y'))



class Actuals(models.Model):
    
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)
    transactions_amount = models.FloatField()
    vendor = models.CharField(max_length = 255,default="")
    details = models.CharField(max_length = 255)

    def __str__(self):
        return self.category.category_feild
