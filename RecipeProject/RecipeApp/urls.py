from django.urls import path
from RecipeApp import views

app_name = "RecipeApp"

urlpatterns = [
    path("", views.main, name="mainpage"),
    path("recipenamelist/", views.RcpNmListView.as_view(), name="rcp_nm_list"),
    path("recipenamelist/detail/<int:pk>", views.RcpDetailView.as_view(), name="rcp_detail"),
    path("tablelist/", views.RcpTableListView.as_view(), name="table_list"),
    
]