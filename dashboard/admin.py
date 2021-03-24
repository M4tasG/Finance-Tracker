from django.contrib import admin
from .models import Classification, Balance, Transaction

# A tad bit more advanced registration of the models to the admin panel, allowing to filter by these categories

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'transaction_class', 'transaction_type', 'amount')

@admin.register(Balance)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'amount')

@admin.register(Classification)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

#admin.site.register(Classification)
#admin.site.register(Balance)
#admin.site.register(Transaction)
