from . import views
from django.urls import path

# URL patterns for the SEO Analyzer app
urlpatterns = [
    # Home page: List of Mainapp entries (user-submitted texts)
    path('', views.mainapp_list, name='mainapp_list'),

    # Form to create a new Mainapp entry (text + optional photo)
    path('create/', views.mainapp_create, name='mainapp_create'),

    # Edit an existing Mainapp entry by its ID
    path('<int:mainapp_id>/edit/', views.mainapp_edit, name='mainapp_edit'),

    # Delete a Mainapp entry by its ID
    path('<int:mainapp_id>/delete/', views.mainapp_delete, name='mainapp_delete'),

    # User registration page
    path('register/', views.register, name='register'),

    # SEO analysis page where the user can input text and view SEO results
    path('seo/', views.analyze_text, name='analyze_text'),

    # You can uncomment and define this route if there's a separate "submit" feature
    # path('submit/', views.submit, name='submit'),
]
