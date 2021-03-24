from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ExpenseForm, LendForm, BorrowForm
from .models import Balance, Transaction, Classification
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
import json


# This is a class based view for displaying all the information on the dashboard
# For Transactions its nearly the same as the default configuration
# but instead of passing a regular queryset, we override the get_queryset method
# this in turn, allows us to filter the queryset by the authenticated user and allows the pagination to work properly
# Later we override get_context_data method to add additional context, these are not paginated
class MainListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'dashboard/main.html'
    context_object_name = 'transactions'
    paginate_by = 5

    def get_queryset(self):
        queryset = Transaction.objects.filter(user = self.request.user).all().order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balances'] = Balance.objects.filter(user = self.request.user).all()
        context['lends'] = Classification.objects.filter(name = "Lend").first().transaction_set.filter(active=True).all()
        context['borrows'] = Classification.objects.filter(name = "Borrow").first().transaction_set.filter(active=True).all()
        context['history_line_start'] = 0
        for x in Balance.objects.filter(user = self.request.user).all():
            context['history_line_start'] += x.amount
        context['history_line_data'] = []
        current_amount = context['history_line_start']
        for x in Transaction.objects.filter(user=self.request.user, time__month=datetime.now().month).all():
            if x.transaction_type == "Spending":
                context['history_line_start'] += x.amount
            else:
                context['history_line_start'] -= x.amount
        current_amount = context['history_line_start']
        context['history_line_data'].append(current_amount)
        for x in Transaction.objects.filter(user=self.request.user, time__month=datetime.now().month).all():
            if x.transaction_type == "Spending":
                current_amount -= x.amount
                context['history_line_data'].append(current_amount)
            else:
                current_amount += x.amount
                context['history_line_data'].append(current_amount)
        # Spendings and Stats calculation
        context['classifications'] = []
        context['amounts'] = []
        context['stats_spend'] = 0
        context['stats_gain'] = 0
        counter = 0
        for x in Classification.objects.filter(user=self.request.user).all():
            """
            # If we wanted to filter out lends and borrows to stats, this is the function for it
            if x.name == "Lend" or x.name == "Borrow":
                pass
            else:
            """
            context['classifications'].append(x.name)
            context['amounts'].append(0)
            for y in Transaction.objects.filter(user=self.request.user, transaction_class=x, time__month=datetime.now().month).all():
                if y.transaction_type == "Spending":
                    context['stats_spend'] += y.amount
                    context['amounts'][counter] += y.amount
                else:
                    context['stats_gain'] += y.amount
                
            counter += 1
        context['classifications'] = json.dumps(context['classifications'])
        context['amounts'] = json.dumps(context['amounts'])
        context['history_line_data'] = json.dumps(context['history_line_data'])
        return context


# Function view for the Expense form
# Using a function view since I could not find a way to do the filling of dropdown lists with a class based view
# This form is first reached with a GET method, therefor just displaying the empty form
# There we pass a request.user argument to be handled in forms.py
# After a user submits the form, the view gets accessed again with POST method
# POST is handled, adding additional information for the user, saving the object and redirecting to the main dashboard
# Mostly the same goes for the gain, lend and borrow forms
@login_required
def new_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.transaction_type = 'Spending'
            form.save()
            return redirect('dashboard-main')
    else:
        form = ExpenseForm(request.user)
    return render(request,'dashboard/expense.html',{'form':form})

@login_required
def new_gain(request):
    if request.method == 'POST':
        form = ExpenseForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.transaction_type = 'Gain'
            form.save()
            return redirect('dashboard-main')
    else:
        form = ExpenseForm(request.user)
    return render(request,'dashboard/gain.html',{'form':form})

@login_required
def new_lend(request):
    if request.method == "POST":
        form = LendForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.transaction_class = Classification.objects.filter(name='Lend').first()
            form.instance.transaction_type = 'Spending'
            form.save()
            return redirect('dashboard-main')
    else:
        form = LendForm(request.user)
    return render(request,'dashboard/lend.html',{'form':form})

@login_required
def new_borrow(request):
    if request.method == "POST":
        form = BorrowForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.transaction_class = Classification.objects.filter(name='Borrow').first()
            form.instance.transaction_type = 'Gain'
            form.save()
            return redirect('dashboard-main')
    else:
        form = BorrowForm(request.user)
    return render(request,'dashboard/borrow.html',{'form':form})

# This is a simple Balance create view, uses a built in class-based generic CreateView
# form_valid method handles the assignment of the balance to the authenticated user

class BalanceCreateView(LoginRequiredMixin ,CreateView):
    model = Balance
    template_name = 'dashboard/balance.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClassificationCreateView(LoginRequiredMixin ,CreateView):
    model = Classification
    template_name = 'dashboard/classification.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Views for the 'Returned' button
# The button directs to a url including the pk of the lend or borrow object
# This view takes the pk and switches the active tag to False on the transaction
# Thus making it not show up in the list of lends and borrows but still show up in the history of transactions

@login_required
def return_lend(request, pk):
    lend = Classification.objects.filter(name='Lend').first().transaction_set.get(pk=pk)
    lend.active = False
    lend.save()
    return redirect('dashboard-main')

@login_required
def return_borrow(request, pk):
    borrow = Classification.objects.filter(name='Borrow').first().transaction_set.get(pk=pk)
    borrow.active = False
    borrow.save()
    return redirect('dashboard-main')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'dashboard/delete.html'
    success_url = reverse_lazy('dashboard-main')

class BalanceDeleteView(DeleteView):
    model = Balance
    template_name = 'dashboard/delete.html'
    success_url = reverse_lazy('dashboard-main')