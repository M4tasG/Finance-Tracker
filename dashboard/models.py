from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Models for the dashboard part of the application
# Currently holding Balance, Classification and Transaction models
# All models currently are related to the user, for customization reasons
# Ex. Users ability to create their own classifications (WORK IN PROGRESS)
# Balance - The users Balance or Balance's
# Transaction - The users Transactions, displayed in the dashboard
# Classification - Used in transaction creation and display to determine their classification


# __str__ functions are used to pass a string when the object is displayed (currently the usage is to pass the name of the object)
# get_absolute_url method will be called on forms, used for redirection

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default="Bank")
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('dashboard-main')

class Classification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default='Utility')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard-main')

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default='Transaction')
    transaction_type = models.CharField(max_length=12, default='Spending', blank=True)
    transaction_class = models.ForeignKey(Classification, on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(default=0)
    #THIS IS FOR LENDS AND BORROWS ONLY SINCE I COULD NOT FIND A WAY TO CRAM ALL THREE MODELS INTO ONE QUERYSET
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard-main')
