from . import views
from django.urls import path


urlpatterns = [
    path('',views.mainapp_list,name='mainapp_list'),    
    path('create/',views.mainapp_create,name='mainapp_create'),
    path('<int:mainapp_id>/edit/',views.mainapp_edit,name='mainapp_edit'),
    path('<int:mainapp_id>/delete/',views.mainapp_delete,name='mainapp_delete'),
    path('register/', views.register,name='register'),
    path('seoapp', views.analyze_text, name='analyze_text'),
    # path('submit/', views.submit,name='submit'),
    
] 