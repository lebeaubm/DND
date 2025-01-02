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
    path('edit_monster/<int:monster_id>/', views.edit_monster, name='edit_monster'),
    path('monsters/', views.monster_list, name='monster_list'),
    path('monster/<int:monster_id>/', views.monster_detail, name='monster_detail'),
    path('basic_monsters/', views.basic_monster_list, name='basic_monster_list'),
    path('basic_monster/<int:monster_id>/', views.basic_monster_detail, name='basic_monster_detail'),

     path('combat_setup/', views.combat_setup, name='combat_setup'),
    path('simulate_combat/', views.simulate_combat, name='simulate_combat'),



]
