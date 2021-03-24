from django.urls import path
from . import views
from .views import MainListView, BalanceCreateView, ClassificationCreateView, TransactionDeleteView, BalanceDeleteView

# URL Patterns for pages
# Class based views are imported and displayed with .as_view() method

# <int:pk> means a primary key is passed into that slot, this is for object selection the view
urlpatterns = [
    path('', MainListView.as_view(), name='dashboard-main'),
    path('create/expense/', views.new_expense, name='dashboard-create-expense'),
    path('create/gain/', views.new_gain, name='dashboard-create-gain'),
    path('create/borrow/', views.new_borrow, name='dashboard-create-borrow'),
    path('create/lend/', views.new_lend, name='dashboard-create-lend'),
    path('create/balance/', BalanceCreateView.as_view(), name='dashboard-create-balance'),
    path('create/classification/', ClassificationCreateView.as_view(), name='dashboard-create-class'),
    path('return/lend/<int:pk>', views.return_lend, name='dashboard-return-lend'),
    path('return/borrow/<int:pk>', views.return_borrow, name='dashboard-return-borrow'),
    path('delete/transaction/<int:pk>', TransactionDeleteView.as_view(), name='dashboard-transaction-delete'),
    path('delete/balance/<int:pk>', BalanceDeleteView.as_view(), name='dashboard-balance-delete'),
]
