from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('', views.index),
    path('authenticate_user', views.authenticate_user),
    path('register', views.register),
    path('create_user', views.create_user),
    path('home', views.recipes),
    path('logout', views.logout),
    path('upload', views.display_upload),
    path('users/<int:id>/upload', views.upload_recipe),
    path('recipes/<int:recipe_id>', views.display_recipe),
    path('<int:recipe_id>/add_likes', views.add_likes),
    path('users/<int:user_id>', views.display_user),
    path('<int:recipe_id>/remove_likes', views.remove_likes),
    path('users/<int:user_id>/edit', views.display_edit_profile),
    path('users/<int:user_id>/update_info', views.update_info),
    path('users/<int:user_id>/update_pw', views.update_pw),
    path('users/<int:user_id>/delete', views.delete_account),
    path('recipes/<int:recipe_id>/delete', views.delete_recipe),
    path('recipes/<int:recipe_id>/edit', views.display_edit_recipe),
    path('recipes/<int:recipe_id>/update', views.update_recipe),
    path('search', views.search),
    path('all_recipes', views.display_all_recipes),
    path('users/<int:user_id>/update_pw', views.update_pw),
]
