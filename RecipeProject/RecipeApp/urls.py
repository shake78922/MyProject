from django.urls import path
from RecipeApp import views

app_name = "RecipeApp"

urlpatterns = [
    path("", views.main, name="mainpage"),
    path("tablelist/", views.RcpTableListView.as_view(), name="table_list"),
    path("recipenamelist/", views.RcpNmListView.as_view(), name="rcp_nm_list"),
    path("recipenamelist/detail/<int:rcp_num>", views.RcpDetailView.as_view(), name="rcp_detail"),
    path("recipenamelist/update/<int:rcp_num>", views.rcp_update_view, name="rcp_update"),
    path("recipenamelist/ingrdnt_create/<int:rcp_num>", views.IngrdntCreateView.as_view(), name="ingrdnt_create"),
    path("recipenamelist/rcp_create/", views.RcpCreateView.as_view(), name="rcp_create"),
    path("recipenamelist/ingrdnt_delete/<int:rcp_num>/<int:pk>", views.IngrdntDeleteView.as_view(), name="ingrdnt_delete"),
    path("recipenamelist/rcp_delete/<int:rcp_num>", views.rcp_delete_view, name="rcp_delete"),
    
    # swagger
    path("tablelist/", views.RcpTableListAPIView.as_view()),
    path("recipenamelist/", views.RcpNmListAPIView.as_view()),
    path("recipenamelist/detail/<int:rcp_num>", views.RcpDetailAPIView.as_view()),
    path("recipenamelist/rcp_create/", views.RcpCreateAPIView.as_view()),
    path("recipenamelist/ingrdnt_create/<int:rcp_num>", views.IngrdntCreateAPIView.as_view()),
    path("recipenamelist/ingrdnt_delete/<int:rcp_num>/<int:pk>", views.IngrdntDeleteAPIView.as_view()),
    path("recipenamelist/rcp_delete/<int:rcp_num>", views.RcpDeleteAPIView.as_view()),
    path("recipenamelist/update/<int:rcp_num>", views.RcpUpdateAPIView.as_view()),
]