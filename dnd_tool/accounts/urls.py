from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Character Sheet URLs
    path('characters/', views.character_list, name='character_list'),
    path('characters/create/', views.character_create, name='character_create'),
    path('characters/<int:sheet_id>/edit/', views.character_edit, name='character_edit'),
    path('characters/<int:sheet_id>/delete/', views.character_delete, name='character_delete'),
    path('upload_monster/', views.upload_monster, name='upload_monster'),
    path('create_monster/', views.create_monster, name='create_monster'),


]
