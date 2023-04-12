from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import RcpTable

# Create your views here.

class RcpTableListView(ListView):
    model = RcpTable