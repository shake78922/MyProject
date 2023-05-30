from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Max, Q
from django.db import transaction
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Recipe, Ingredient
from .forms import IngredientCreateForm, RcpFormsetForm, RcpFormSet
from .serializers import RcpTableSerializer


def search_recipe_from_ingredient(searchword):
    """ 검색 키워드에 맞는 재료명들의 레시피명을 쿼리셋으로 반환해주는 메서드"""
    rcp_qs = Recipe.objects.all()
    container_qs = Recipe.objects.none()
    for obj1 in rcp_qs:
        tmp_qs1 = obj1.ingredient.filter(Q(name__icontains=searchword))
        for obj2 in tmp_qs1:
            tmp_qs2 = Recipe.objects.filter(id=obj2.rcp.id)
            container_qs = container_qs | tmp_qs2
    return container_qs

# 메인 페이지
def main(request):
    return render(request,"RecipeApp/mainpage.html")


""" Django CBV & FBV 뷰 """

# 레시피명 리스트 뷰
class RecipeListView(ListView):
    # 속성
    model = Recipe
    template_name = 'RecipeApp/recipe_list.html'
    context_object_name = 'recipe_list'
    paginate_by = 10
    
    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        context = super(RecipeListView, self).get_context_data(**kwargs)
        
        # 페이징 정보 context
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=2)
        context['pagelist'] = pagelist
        
        # 검색 정보 context
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        return context
    
    # 쿼리셋 호출 메서드
    def get_queryset(self, *args, **kwargs):
        
        # 검색에 필요한 변수
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        
        # 레시피 번호 기준으로 역순 정렬 후 중복값을 제외한 전체 테이블 쿼리셋
        queryset = super(RecipeListView, self).get_queryset(*args, **kwargs)
        queryset = queryset1.order_by("-id") # .distinct('rcp_num')
        
        # 검색 기능
        if search_keyword:
            # 검색 키워드 2글자 이상
            if len(search_keyword) > 1:
                # 검색 키워드가 숫자일 경우
                # if search_keyword.isdigit():
                # 전체 검색
                if search_type == 'all':
                    queryset1 = queryset.filter(
                        Q(id__icontains=search_keyword) |
                        Q(name__icontains=search_keyword))
                    queryset2 = search_recipe_from_ingredient(search_keyword)
                    search_list = queryset1 | queryset2

                # 레시피 번호 검색
                elif search_type == 'rcp_id':
                    search_list = queryset.filter(id__exact=search_keyword)
                # 레시피 이름 검색
                elif search_type == 'rcp_name':
                    search_list = queryset.filter(name__icontains=search_keyword)
                # 재료 이름 검색
                elif search_type == 'ingredient_name':
                    search_list = search_recipe_from_ingredient(search_keyword)
                return search_list
            # 검색 키워드 2글자 이하
            else:
                messages.error(self.request, '검색어를 2글자 이상 입력하세요.')
        return queryset


# 전체 테이블 리스트 뷰
class IngredientListView(ListView):
    # 속성
    model = Ingredient
    template_name = 'RecipeApp/ingredient_list.html'
    context_object_name = 'ingredient_list'
    paginate_by = 10
    
    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        
        # 페이징 정보 context 추가
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=2)
        context['pagelist'] = pagelist
        
        # 검색 정보 context 추가
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        context['type'] = search_type
        if len(search_keyword) > 1:
            context['q'] = search_keyword
        return context
    
    # 쿼리셋 호출 메서드
    def get_queryset(self, *args, **kwargs):
        
        # 검색에 필요한 변수
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        
        # 고유키 기준 역순으로 정렬한 전체 테이블 쿼리셋
        queryset = super(IngredientListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.order_by("-id")
        
        # 검색 기능
        if search_keyword:
            # 검색 키워드 2글자 이상
            if len(search_keyword) > 1:
                # 검색 키워드가 숫자일 경우
                # if search_keyword.isdigit():
                # 전체 검색
                if search_type == 'all':
                    search_list = queryset.filter(
                        Q(id__icontains=search_keyword) |
                        Q(name__icontains=search_keyword))
                # 재료 고유키 검색
                elif search_type == 'ingredient_id':
                    search_list = queryset.filter(id__exact=search_keyword)
                # 재료 이름 검색
                elif search_type == 'ingredient_name':
                    search_list = queryset.filter(name__icontains=search_keyword)
                return search_list
            # 검색 키워드 2글자 이하
            else:
                messages.error(self.request, '검색어를 2글자 이상 입력하세요.')
        return queryset


# 레시피별 재료 (상세)리스트 뷰
class RecipeDetailView(DetailView):
    # 속성
    model = Recipe
    template_name = 'RecipeApp/recipe_detail.html'
    
    # 쿼리셋 호출 메서드
    def get_queryset(self, *args, **kwargs):
        # (URL 파라미터 값 = 레시피 번호)에 해당하는 데이터 필터링 후 정렬한 쿼리셋
        rcp_id = self.kwargs['id']
        # queryset = super(RecipeDetailView, self).get_queryset(*args, **kwargs)
        recipe = Recipe.objects.get(id=rcp_id)
        queryset = recipe.ingredient.order_by('id')
        return queryset
    
    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        rcp_id = self.kwargs['id']
        recipe = Recipe.objects.get(id=rcp_id)
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        context['recipe'] = recipe
        context['ingredients'] = self.get_queryset()
        return context


# 레시피별 수정 메서드 (FBV)
def rcp_update_view(request, rcp_num):
    queryset = RcpTable.objects.filter(rcp_num=rcp_num).order_by('rcp_sub_num')
    rcp_detail = RcpTable.objects.filter(rcp_num=rcp_num).order_by('rcp_sub_num')
    recipe_name = rcp_detail[0]

    if request.method == 'POST':
        update_queries = []
        for rcp_item in queryset:
            rcp_item.rcp_nm = request.POST.get('rcp_nm_' + str(rcp_item.rcp_num))
            rcp_item.rcp_sub_num = request.POST.get('rcp_sub_num_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_sub_nm = request.POST.get('rcp_sub_nm_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_nm = request.POST.get('rcp_ingrdnt_nm_' + str(rcp_item.rcp_pk))
            rcp_item.rcp_ingrdnt_qnt = request.POST.get('rcp_ingrdnt_qnt_' + str(rcp_item.rcp_pk)) or ""
            rcp_item.rcp_ingrdnt_unit = request.POST.get('rcp_ingrdnt_unit_' + str(rcp_item.rcp_pk)) or ""
            rcp_item.rcp_ingrdnt_sub = request.POST.get('rcp_ingrdnt_sub_' + str(rcp_item.rcp_pk)) or ""
            update_queries.append(rcp_item)
        RcpTable.objects.bulk_update(update_queries, ['rcp_nm','rcp_sub_num', 'rcp_sub_nm', 'rcp_ingrdnt_nm', 'rcp_ingrdnt_qnt', 'rcp_ingrdnt_unit', 'rcp_ingrdnt_sub'])
        return HttpResponseRedirect(reverse_lazy('RecipeApp:rcp_detail', kwargs={'rcp_num': rcp_num}))

    context = {
        'rcp_num': rcp_num,
        'rcp_detail': rcp_detail,
        'recipe_name': recipe_name,
    }
    return render(request, 'RecipeApp/rcp_update.html', context)


# 기존 레시피의 재료 생성 뷰
class IngredientCreateView(CreateView):
    # 속성
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'RecipeApp/ingrdnt_create.html'
    
    # 폼에서 사용할 초기 데이터 반환
    def get_initial(self):
        # (URL 파라미터 값 = 레시피 번호)에 해당하는 레시피의 상세 페이지에서 마지막 순번의 재료 번호 + 1 값을 새로 생성되는 폼의 초기값으로 반환
        rcp_num = self.kwargs['rcp_num']
        last_rcp_sub_num = Ingredient.objects.filter(rcp_num=rcp_num)
        last_rcp_sub_num = last_rcp_sub_num.aggregate(Max('rcp_sub_num'))['rcp_sub_num__max'] + 1
        return {'rcp_sub_num': last_rcp_sub_num}
    
    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        rcp_num = self.kwargs['rcp_num']
        context = super(IngredientCreateView, self).get_context_data(**kwargs)
        context['rcp_num'] = rcp_num
        context['rcp_detail'] = Ingredient.objects.filter(rcp_num=rcp_num).order_by('rcp_sub_num')
        context['recipe_name'] = context['rcp_detail'][0]
        return context
    
    # 처리 성공 URL 호출 메서드
    def get_success_url(self):
        rcp_num = self.kwargs['rcp_num']
        success_url = reverse_lazy('RecipeApp:rcp_detail', kwargs={'rcp_num': rcp_num})
        return success_url

    # 폼 데이터 처리 메서드
    def form_valid(self, form):
        # 폼이 유효할 경우
        if form.is_valid():
            #(URL 파라미터 값 = 레시피 번호) 클릭한 레시피의 마지막 재료
            rcp_num = self.kwargs['rcp_num']
            last_ingrdnt = Ingredient.objects.all().order_by('rcp_pk').last()
            # 작성된 폼에서 PK와 HiddenInput field에 값을 넣어줌
            form.instance = form.save(commit=False)
            form.instance.rcp_pk = last_ingrdnt.rcp_pk + 1
            form.instance.rcp_num = rcp_num
            form.instance.rcp_nm = RcpTable.objects.filter(rcp_num=rcp_num).first().rcp_nm
            form.instance.rcp_ingrdnt_qnt = form.instance.rcp_ingrdnt_qnt or ""
            form.instance.rcp_ingrdnt_unit = form.instance.rcp_ingrdnt_unit or ""
            form.instance.rcp_ingrdnt_sub = form.instance.rcp_ingrdnt_sub or ""
            form.instance.created_by = self.request.user
            # 폼 인스턴스 저장
            form.instance.save()
            return super().form_valid(form)
        
        # 폼이 유효하지 않을 경우
        else:
            return self.form_invalid(form)


# 레시피 생성 뷰
class RcpCreateView(CreateView):
    # 속성
    model = RcpTable
    form_class = RcpFormsetForm
    template_name = 'RecipeApp/rcp_create.html'
    
    # 유효하지 않은 폼 데이터 처리 메서드
    def form_invalid(self, form, formset):
        return self.render_to_response({'formset':formset})
    
    # 처리 성공 URL 호출 메서드
    def get_success_url(self):
        return reverse_lazy('RecipeApp:rcp_nm_list')
    
    # GET 요청 처리 메서드
    def get(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = RcpFormSet(queryset=RcpTable.objects.none(), initial=[{'rcp_sub_num': 1}])
        return self.render_to_response({'form':form, 'formset':formset})
    
    # POST 요청 처리 메서드
    def post(self, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
        formset = RcpFormSet(data=self.request.POST)
        
        rcp_inst_name = self.request.POST.get('rcp_inst_nm')
        if RcpTable.objects.filter(rcp_nm=rcp_inst_name).exists():
            messages.error(self.request, '이미 존재하는 레시피 이름입니다.')
            return self.form_invalid(form, formset)
    
        last_rcp_pk = RcpTable.objects.aggregate(Max('rcp_pk'))['rcp_pk__max']
        last_rcp_num = RcpTable.objects.aggregate(Max('rcp_num'))['rcp_num__max']
        
        instances = formset.save(commit=False)
        for i, instance in enumerate(instances):
            instance.rcp_pk = last_rcp_pk + (i+1)
            instance.rcp_num = last_rcp_num + 1
            instance.rcp_nm = rcp_inst_name
            instance.rcp_ingrdnt_qnt = instance.rcp_ingrdnt_qnt or ""
            instance.rcp_ingrdnt_unit = instance.rcp_ingrdnt_unit or ""
            instance.rcp_ingrdnt_sub = instance.rcp_ingrdnt_sub or ""
            
            if instance.rcp_sub_num == None or instance.rcp_sub_num == "":
                messages.error(self.request, '재료 번호를 입력하세요.')
                return self.form_invalid(form, formset)
            
            if instance.rcp_sub_nm == None or instance.rcp_sub_nm == "":
                messages.error(self.request, '단계명을 입력하세요.')
                return self.form_invalid(form, formset)
            
            if instance.rcp_ingrdnt_nm == None or instance.rcp_ingrdnt_nm == "":
                messages.error(self.request, '재료명을 입력하세요.')
                return self.form_invalid(form, formset)
            
        with transaction.atomic():
            formset.save()

        if formset.is_valid():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form, formset)


# 재료 삭제 뷰
class IngrdntDeleteView(DeleteView):
    # 속성
    model = RcpTable
    context_object_name = 'rcp_item'
    template_name = 'RecipeApp/ingrdnt_delete.html'

    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        rcp_pk = self.kwargs['pk']
        context = super(IngrdntDeleteView, self).get_context_data(**kwargs)
        obj = RcpTable.objects.get(rcp_pk=rcp_pk)
        context['rcp_item'] = obj
        context['name'] = obj.__str__()
        return context
    
    # 처리 성공 URL 호출 메서드
    def get_success_url(self):
        # 재료가 삭제된 후에도 레시피 안에 다른 재료가 남아있을 경우 해당 레시피 상세 페이지로 리디렉션
        rcp_num = self.kwargs['rcp_num']
        if RcpTable.objects.filter(rcp_num=rcp_num).exists():
            return reverse_lazy('RecipeApp:rcp_detail', kwargs={'rcp_num': rcp_num})
        
        # 레시피의 마지막 재료가 삭제됐을 경우 레시피 리스트뷰 페이지로 리디렉션
        else:
            return reverse_lazy('RecipeApp:rcp_nm_list')
    
    # POST 요청 처리 메서드
    def post(self, request, *args, **kwargs):
        rcp_pk = self.kwargs['pk']
        rcp_num = self.kwargs['rcp_num']
        
        # 재료 삭제
        target_ingrdnt = RcpTable.objects.get(rcp_pk=rcp_pk)
        rcp_sub_num = target_ingrdnt.rcp_sub_num
        target_ingrdnt.delete()
        
        # 삭제된 재료보다 밑에 있는 재료들의 재료 번호를 하나씩 위로 옮김
        if RcpTable.objects.filter(rcp_sub_num__gt=rcp_sub_num).exists():
            ingrdnt_shift = RcpTable.objects.filter(rcp_num=rcp_num)
            ingrdnt_shift = ingrdnt_shift.filter(rcp_sub_num__gt=rcp_sub_num)
            for ingrdnt in ingrdnt_shift:
                ingrdnt.rcp_sub_num -= 1
                ingrdnt.save()
        return HttpResponseRedirect(self.get_success_url())


# 레시피 삭제 메서드 (FBV)
def rcp_delete_view(request, rcp_num):
    rcp_item = RcpTable.objects.filter(rcp_num=rcp_num)
    rcp_nm = rcp_item[0].rcp_nm

    if request.method == 'POST':
        rcp_item.delete()
        if RcpTable.objects.filter(rcp_num__gt=rcp_num).exists():
            rcp_shift = RcpTable.objects.filter(rcp_num__gt=rcp_num)
            for ingrdnt in rcp_shift:
                ingrdnt.rcp_num -= 1
                ingrdnt.save()
        return HttpResponseRedirect(reverse_lazy('RecipeApp:rcp_nm_list'))

    context = {
        'rcp_item': rcp_item,
        'rcp_nm': rcp_nm,
    }

    return render(request, 'RecipeApp/rcp_delete.html', context)



""" DRF API 뷰 """


# swagger

# 전체 테이블 리스트 API뷰
class RcpTableListAPIView(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer


# 레시피명 리스트 API 뷰
class RcpNmListAPIView(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer


# 레시피별 상세 API 뷰
class RcpDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()
    lookup_field = 'rcp_num'
    
    
# 레시피 생성 API 뷰
class RcpCreateAPIView(generics.CreateAPIView):
    # 속성
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()

    # 폼 데이터 처리 메서드
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 레시피 이름 중복 여부 확인
        rcp_nm = serializer.validated_data['rcp_nm']
        if RcpTable.objects.filter(rcp_nm=rcp_nm).exists():
            return Response({'error': '이미 존재하는 레시피 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 PK와 레시피 번호 부여 (마지막 번호 + 1)
        last_rcp_pk = RcpTable.objects.aggregate(Max('rcp_pk'))['rcp_pk__max']
        serializer.validated_data['rcp_pk'] = last_rcp_pk + 1
        last_rcp_num = RcpTable.objects.aggregate(Max('rcp_num'))['rcp_num__max']
        serializer.validated_data['rcp_num'] = last_rcp_num + 1

        # 레시피 생성
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

# 재료 생성 API 뷰
class IngrdntCreateAPIView(generics.CreateAPIView):
    # 속성
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()
    lookup_field = 'rcp_num'

    # 폼 데이터 처리 메서드
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 레시피 번호에 해당하는 레시피가 존재하는지 확인
        rcp_num = serializer.validated_data['rcp_num']
        if not RcpTable.objects.filter(rcp_num=rcp_num).exists():
            return Response({'error': '존재하지 않는 레시피 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 PK와 재료 번호 부여 (마지막 번호 + 1)
        last_rcp_pk = RcpTable.objects.aggregate(Max('rcp_pk'))['rcp_pk__max']
        serializer.validated_data['rcp_pk'] = last_rcp_pk + 1
        last_rcp_sub_num = RcpTable.objects.filter(rcp_num=rcp_num).aggregate(Max('rcp_sub_num'))['rcp_sub_num__max']
        if last_rcp_sub_num is None:
            last_rcp_sub_num = 0
        serializer.validated_data['rcp_sub_num'] = last_rcp_sub_num + 1

        # 재료 생성
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
# 재료 삭제 API 뷰
class IngrdntDeleteAPIView(generics.DestroyAPIView):
    # 속성
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()
    lookup_field = 'rcp_num', 'rcp_pk'

    # 처리 성공 응답 메서드
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        rcp_num = instance.rcp_num

        # 재료 삭제
        self.perform_destroy(instance)

        # 삭제된 재료보다 밑에 있는 재료들의 재료 번호를 하나씩 위로 옮김
        if RcpTable.objects.filter(rcp_num=rcp_num).exists():
            ingrdnt_shift = RcpTable.objects.filter(rcp_num=rcp_num)
            ingrdnt_shift = ingrdnt_shift.filter(rcp_sub_num__gt=instance.rcp_sub_num)
            for ingrdnt in ingrdnt_shift:
                ingrdnt.rcp_sub_num -= 1
                ingrdnt.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 레시피 삭제 API 뷰
class RcpDeleteAPIView(generics.DestroyAPIView):
    # 속성
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()
    lookup_field = 'rcp_num'

    # 처리 성공 응답 메서드
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        rcp_num = instance.rcp_num

        # 레시피 삭제
        self.perform_destroy(instance)

        # 삭제된 레시피보다 높은 레시피들의 레시피 번호를 하나씩 아래로 옮김
        if RcpTable.objects.filter(rcp_num__gt=rcp_num).exists():
            rcp_shift = RcpTable.objects.filter(rcp_num__gt=rcp_num)
            for ingrdnt in rcp_shift:
                ingrdnt.rcp_num -= 1
                ingrdnt.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 레시피 수정 API 뷰
class RcpUpdateAPIView(generics.UpdateAPIView):
    # 속성
    serializer_class = RcpTableSerializer
    queryset = RcpTable.objects.all()
    lookup_field = 'rcp_num'

    # 폼 데이터 처리 메서드
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 레시피 이름 중복 여부 확인
        rcp_nm = serializer.validated_data['rcp_nm']
        if RcpTable.objects.filter(rcp_nm=rcp_nm).exclude(rcp_pk=instance.rcp_pk).exists():
            return Response({'error': '이미 존재하는 레시피 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 레시피 수정
        self.perform_update(serializer)
        return Response(serializer.data)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




# UpdateView 클라스뷰 대신 함수뷰로 수정
"""
class RcpUpdateView(ListView):
    
    # 속성
    model = RcpTable
    template_name = 'RecipeApp/rcp_update.html'
    
    # 쿼리셋 호출 메서드
    def get_queryset(self, *args, **kwargs):
        # (URL 파라미터 값 = 레시피 번호)에 해당하는 데이터 필터링 후 정렬한 쿼리셋
        rcp_num = self.kwargs['rcp_num']
        queryset = super(RcpUpdateView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(rcp_num=rcp_num).order_by('rcp_sub_num')
        return queryset

    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        rcp_num = self.kwargs['rcp_num']
        context = super(RcpUpdateView, self).get_context_data(**kwargs)
        context['rcp_num'] = rcp_num
        context['rcp_detail'] = RcpTable.objects.filter(rcp_num=rcp_num).order_by('rcp_sub_num')
        context['recipe_name'] = context['rcp_detail'][0]
        return context
    
    # 처리 성공 URL 호출 메서드
    def get_success_url(self):
        rcp_num = self.kwargs['rcp_num']
        success_url = reverse_lazy('RecipeApp:rcp_detail', kwargs={'rcp_num': rcp_num})
        return success_url

    # POST 요청 처리 메서드
    def post(self, request, *args, **kwargs):
        rcp_num = self.kwargs['rcp_num']
        queryset = self.get_queryset()
        # 객체 존재 여부 확인
        if queryset.exists() == True:
            update_queries = []
            # 기존 쿼리셋 데이터의 field 마다 폼으로 받은 POST 요청 데이터로 수정
            for rcp_item in queryset:
                rcp_item.rcp_num = rcp_num
                rcp_item.rcp_nm = request.POST.get('rcp_nm_' + str(rcp_item.rcp_num))
                rcp_item.rcp_sub_num = request.POST.get('rcp_sub_num_' + str(rcp_item.rcp_pk))
                rcp_item.rcp_sub_nm = request.POST.get('rcp_sub_nm_' + str(rcp_item.rcp_pk))
                rcp_item.rcp_ingrdnt_nm = request.POST.get('rcp_ingrdnt_nm_' + str(rcp_item.rcp_pk))
                rcp_item.rcp_ingrdnt_qnt = request.POST.get('rcp_ingrdnt_qnt_' + str(rcp_item.rcp_pk))
                rcp_item.rcp_ingrdnt_unit = request.POST.get('rcp_ingrdnt_unit_' + str(rcp_item.rcp_pk))
                rcp_item.rcp_ingrdnt_sub = request.POST.get('rcp_ingrdnt_sub_' + str(rcp_item.rcp_pk))
                # update_queries 리스트에 수정된 데이터 객체 삽입
                update_queries.append(rcp_item)
            # bulk_update 메서드로 수정된 객체들을 한꺼번에 수정   
            RcpTable.objects.bulk_update(update_queries, ['rcp_nm','rcp_sub_num', 'rcp_sub_nm', 'rcp_ingrdnt_nm', 'rcp_ingrdnt_qnt', 'rcp_ingrdnt_unit', 'rcp_ingrdnt_sub'])  
        return HttpResponseRedirect(self.get_success_url())"""



# DeleteView 클라스뷰 대신 함수뷰로 수정      
"""
class RcpDeleteView(ListView):
    
    # 속성
    model = RcpTable
    context_object_name = 'rcp_item'
    template_name = 'RecipeApp/rcp_delete.html'
    success_url = reverse_lazy('RecipeApp:rcp_nm_list')
    
    # context 데이터 호출 메서드
    def get_context_data(self, **kwargs):
        rcp_num = self.kwargs['rcp_num']
        context = super(RcpDeleteView, self).get_context_data(**kwargs)
        rcp_nm = RcpTable.objects.filter(rcp_num=rcp_num)[0].rcp_nm
        context['rcp_nm'] = rcp_nm
        return context
    
    # POST 요청 처리 메서드
    def post(self, request, *args, **kwargs):
        rcp_num = self.kwargs['rcp_num']
        
        # 레시피 삭제
        target_rcp = RcpTable.objects.filter(rcp_num=rcp_num)
        target_rcp.delete()
        
        # 삭제된 레시피보다 밑에 있는 레시피들의 레시피 번호를 하나씩 위로 옮김
        if RcpTable.objects.filter(rcp_num__gt=rcp_num).exists():
            rcp_shift = RcpTable.objects.filter(rcp_num__gt=rcp_num)
            for ingrdnt in rcp_shift:
                ingrdnt.rcp_num -= 1
                ingrdnt.save()
        return HttpResponseRedirect(self.success_url)"""
        
        
        
        
        
        
        
        
        
        
        
"""class RcpTableList(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer

class RcpNmList(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer

class RcpCreate(generics.CreateAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer

class IngrdntCreate(generics.CreateAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer
    lookup_field = 'rcp_num'

class RcpDetail(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer
    lookup_field = 'rcp_num'

class RcpUpdate(generics.UpdateAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer
    lookup_field = 'rcp_num'
    
class IngrdntDelete(generics.DestroyAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer
    lookup_field = 'rcp_num', 'pk'

class RcpDelete(generics.ListAPIView):
    queryset = RcpTable.objects.all()
    serializer_class = RcpTableSerializer
    lookup_field = 'rcp_num'"""