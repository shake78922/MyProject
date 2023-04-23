from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import RcpTable
from .forms import IngrdntCreateForm, RcpCreateForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import Max
from django import forms


# Create your views here.

def main(request):
    return render(request,"RecipeApp/mainpage.html")

class RcpNmListView(ListView):
    model = RcpTable
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
    
    def get_queryset(self, *args, **kwargs):
        qs = super(RcpNmListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-rcp_num").distinct('rcp_num').all()
        return qs

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
    
    def get_queryset(self, *args, **kwargs):
        qs = super(RcpTableListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-rcp_pk")
        return qs
    
class RcpDetailView(DetailView):
    model = RcpTable
    template_name = 'RecipeApp/rcp_detail.html'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(RcpDetailView, self).get_context_data(**kwargs)
        context['pk'] = pk
        context['rcp_detail'] = RcpTable.objects.filter(rcp_num=pk).order_by('rcp_sub_num')
        context['recipe_name'] = context['rcp_detail'][0]
        return context

class RcpUpdateView(UpdateView):
    model = RcpTable
    fields = ['rcp_nm','rcp_sub_nm', 'rcp_ingrdnt_nm', 'rcp_ingrdnt_qnt', 'rcp_ingrdnt_unit', 'rcp_ingrdnt_sub']
    template_name = 'RecipeApp/rcp_update.html'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(RcpUpdateView, self).get_context_data(**kwargs)
        context['pk'] = pk
        context['rcp_detail'] = RcpTable.objects.filter(rcp_num=pk).order_by('rcp_sub_num')
        context['recipe_name'] = context['rcp_detail'][0]
        return context
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('RecipeApp:rcp_detail', kwargs={'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        rcp_detail = RcpTable.objects.filter(rcp_num=pk).order_by('rcp_sub_num')
        for rcp_item in rcp_detail:
            rcp_item.rcp_nm = request.POST.get('rcp_nm_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_sub_num = request.POST.get('rcp_sub_num_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_sub_nm = request.POST.get('rcp_sub_nm_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_nm = request.POST.get('rcp_ingrdnt_nm_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_qnt = request.POST.get('rcp_ingrdnt_qnt_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_unit = request.POST.get('rcp_ingrdnt_unit_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_sub = request.POST.get('rcp_ingrdnt_sub_' + str(rcp_item.rcp_pk))
            rcp_item.save()
        return HttpResponseRedirect(self.get_success_url())

class IngrdntCreateView(CreateView):
    model = RcpTable
    form_class = IngrdntCreateForm
    template_name = 'RecipeApp/ingrdnt_create.html'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(IngrdntCreateView, self).get_context_data(**kwargs)
        context['pk'] = pk
        context['rcp_detail'] = RcpTable.objects.filter(rcp_num=pk).order_by('rcp_sub_num')
        context['recipe_name'] = context['rcp_detail'][0]
        return context
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('RecipeApp:rcp_detail', kwargs={'pk': pk})

    def form_valid(self, form):
        if form.is_valid():
            rcp_num = self.kwargs['pk']
            last_ingrdnt = RcpTable.objects.filter(rcp_num=rcp_num).order_by('-rcp_pk').first()
            form.instance.rcp_pk = last_ingrdnt.rcp_pk + 1
            form.instance.rcp_num = rcp_num
            form.instance.rcp_nm = RcpTable.objects.filter(rcp_num=rcp_num).first().rcp_nm
            form.instance = form.save(commit=False)
            form.instance.created_by = self.request.user
            form.instance.save()
            ingrdnts_to_shift = RcpTable.objects.filter(rcp_pk__gte=form.instance.rcp_pk).exclude(pk=form.instance.pk)
            for ingrdnt in ingrdnts_to_shift:
                ingrdnt.rcp_pk += 1
                ingrdnt.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
class RcpCreateView(CreateView):
    model = RcpTable
    form_class = RcpCreateForm
    template_name = 'RecipeApp/rcp_create.html'
    success_url = reverse_lazy('RecipeApp:rcp_nm_list')
    
    def get_initial(self):
        return {'rcp_sub_num': 1}

    def form_valid(self, form):
        if form.is_valid():
            rcp_nm = form.cleaned_data['rcp_nm']
            if RcpTable.objects.filter(rcp_nm=rcp_nm).exists():
                form.add_error('rcp_nm', '이미 존재하는 레시피 이름입니다.')
                return self.form_invalid(form)
            form.instance = form.save(commit=False)
            last_rcp_pk = RcpTable.objects.aggregate(Max('rcp_pk'))['rcp_pk__max']
            form.instance.rcp_pk = last_rcp_pk + 1
            last_rcp_num = RcpTable.objects.aggregate(Max('rcp_num'))['rcp_num__max']
            form.instance.rcp_num = last_rcp_num + 1
            form.instance.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class IngrdntDeleteView(DeleteView):
    pass

class RcpDeleteView(DeleteView):
    pass
