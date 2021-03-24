from django.forms import ModelForm
from .models import Classification, Balance, Transaction
from django.db.models import Q

# Tbh? I have NO FUCKING CLUE what I did here
# Mostly just ripping off code from stackoverflow (actually all of it but I removed the unecessary parts)
# The form class is pretty self explanatory
# __init__ method handles the dropdown fields being prefilled with the user data
# Why is it __init__? again, not a slightest idea but it works
# Anyway, __init__ gets called, super() calls the implementation of parent class
# Then with self.fields['x'].queryset we filter the queryset of that field with the user argument which gets passed in as request.user
# Meta class is just for the form definition itself
# Uses the Transaction model, has the fields that only the user needs to see.

class ExpenseForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['balance'].queryset=Balance.objects.filter(user=user).all()
        self.fields['transaction_class'].queryset=Classification.objects.filter(user=user).exclude(Q(name='Lend') | Q(name='Borrow')).all()
    
    class Meta:
        model = Transaction
        fields = ('name','balance','transaction_class','amount')

class LendForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(LendForm, self).__init__(*args, **kwargs)
        self.fields['balance'].queryset=Balance.objects.filter(user=user).all()

    class Meta:
        model = Transaction
        fields = ('name','balance','amount')

class BorrowForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)
        self.fields['balance'].queryset=Balance.objects.filter(user=user).all()

    class Meta:
        model = Transaction
        fields = ('name','balance','amount')

