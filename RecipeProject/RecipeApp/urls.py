from django.urls import path
from RecipeApp import views

app_name = "RecipeApp"

urlpatterns = [
    path("", views.main, name="mainpage"),
    path("tablelist/", views.RcpTableListView.as_view(), name="table_list"),
    path("recipenamelist/", views.RcpNmListView.as_view(), name="rcp_nm_list"),
    path("recipenamelist/detail/<int:pk>", views.RcpDetailView.as_view(), name="rcp_detail"),
    path("recipenamelist/update/<int:pk>", views.RcpUpdateView.as_view(), name="rcp_update"),
    path("recipenamelist/ingrdnt_create/<int:pk>", views.IngrdntCreateView.as_view(), name="ingrdnt_create"),
    path("recipenamelist/rcp_create/", views.RcpCreateView.as_view(), name="rcp_create"),
    path("recipenamelist/ingrdnt_delete/<int:pk>", views.IngrdntDeleteView.as_view(), name="ingrdnt_delete"),
    path("recipenamelist/rcp_delete/<int:pk>", views.RcpDeleteView.as_view(), name="rcp_delete"),
]