from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecord
from .models import Record
# Create your views here.

def home(request):
    records = Record.objects.all()
    
    if request.method=='POST':
       username= request.POST["username"]
       password= request.POST["password"]
       user =authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user) 
           messages.success(request, "You have been logged in Successfully")
           return redirect('home')
       else:
           messages.success(request, "Invalid username or password")
           return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})
def login_user(request):
    pass
def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out ...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            user= authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect('home')
    else:
        form= SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be logged in . . .")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, f"Record {pk} is deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in . . .")
        return redirect('home')
def add_record(request):
    form=AddRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                form.save()
                messages.success(request, f"Record is added successfully")
                return redirect('home')
        return render(request, 'add.html', {'form': form})
    else:
        messages.success(request, "You must be logged in . . .")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        form=AddRecord(request.POST or None, instance=customer_record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record is updated successfully")
            return redirect('home')
        else:
            return render(request, 'update.html', {'form': form})
    else:
        messages.success(request, "You must be logged in . . .")
        return redirect('home')