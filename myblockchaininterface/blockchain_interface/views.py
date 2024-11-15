from django.shortcuts import render

def home(request):
    return render(request, 'blockchain_interface/home.html')

def view_records(request):
    return render(request, 'blockchain_interface/view_records.html')

def edit_record(request):
    return render(request, 'blockchain_interface/edit_record.html')

def view_history(request):
    return render(request, 'blockchain_interface/history.html')

def add_record(request):
    return render(request, 'blockchain_interface/add_record.html')
