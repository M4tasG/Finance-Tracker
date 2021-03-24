from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction,  Balance, Classification
from django.contrib.auth.models import User
import math

# This file handles the signals

# !THIS FILE HAS TO BE IMPORTED IN THE CONFIG (LOCATED IN apps.py)!

# When a transaction is being created, a post_save signal is being sent
# This function handles the post_save and updates the balance that is being interacted with
# Sender = the model that sends the signal
# Instance = The object of the model that sent the signal
# Created = A Boolean which is false if the transaction is just being saved and not created
@receiver(post_save, sender=Transaction)
def balance_update_post_transaction(sender, instance, created, **kwargs):
    if created:
        transaction = instance
        balance_updated = transaction.balance
        if(transaction.transaction_type == "Spending"):
            balance_updated.amount = round(balance_updated.amount - transaction.amount, 2)
            balance_updated.save()
        else:
            balance_updated.amount = round(balance_updated.amount + transaction.amount, 2)
            balance_updated.save() 
        
# This function creates the basic classifications for the user after their account is created
@receiver(post_save, sender=User)
def classification_create_post_registration(sender, instance, created, **kwargs):
    if created:
        new_classification = Classification(name = 'Utility', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Lend', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Borrow', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Food', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Entertainment', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Transport', user=instance)
        new_classification.save()
        new_classification = Classification(name = 'Bills', user=instance)
        new_classification.save()
