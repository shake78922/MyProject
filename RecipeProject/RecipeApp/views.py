from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *

# Create your views here.

def main(request):
    return render(request,"RecipeApp/mainpage.html")

class RcpNmListView(ListView):
    model = RcpNmTable
    template_name = 'RecipeApp/rcp_nm_list.html'
    context_object_name = 'rcp_nm_list'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(RcpNmListView, self).get_context_data(**kwargs)
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=2)
        context['pagelist'] = pagelist
        return context

class RcpTableListView(ListView):
    model = RcpTable
    context_object_name = 'table_list'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super(RcpTableListView, self).get_context_data(**kwargs)
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=2)
        context['pagelist'] = pagelist
        return context
    
class RcpDetailView(DetailView):
    model = RcpTable
    template_name = 'RecipeApp/rcp_detail.html'
    context_object_name = 'rcp_detail'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(RcpDetailView, self).get_context_data(**kwargs)
        context['pk'] = pk
        context['object'] = RcpTable.objects.filter(rcp_nm_fk=pk)
        return context
    
    
"""    def get_context_data(self, **kwargs):
        context = super(RcpDetailView, self).get_context_data(**kwargs)
        context['rcp_detail'] = RcpTable.object.filter(rcp_pk=self.kwargs['pk'])
        return context"""
    

    
    