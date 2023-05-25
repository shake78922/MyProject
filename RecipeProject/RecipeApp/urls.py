from django.urls import path
from RecipeApp import views

app_name = "RecipeApp"

urlpatterns = [
    path("", views.main, name="mainpage"),
    path("ingredients", views.IngredientListView.as_view(), name="ingredient_list"),
    path("recipes", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<int:id>", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipes/<int:id>", views.rcp_update_view, name="rcp_update"),
    path("recipes/<int:id>", views.IngredientCreateView.as_view(), name="ingredient_create"),
    path("recipes", views.RcpCreateView.as_view(), name="rcp_create"),
    path("ingredients/<int:id>", views.IngrdntDeleteView.as_view(), name="ingrdnt_delete"),
    path("recipes/<int:id>", views.rcp_delete_view, name="rcp_delete"),
    
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
namespace='RecipeApp'
