from django.urls import path
from RecipeApp import views

app_name = "RecipeApp"

urlpatterns = [
    path("",views.RcpTableListView.as_view(),name="table_list"),
    # path('upload_images/', views.UploadImage.as_view(),name='upload_images_url'),
    
]