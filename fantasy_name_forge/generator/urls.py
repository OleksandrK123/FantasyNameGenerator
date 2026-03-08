from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('logout/', views.custom_logout, name='logout'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('my-names/', views.my_favorites, name='my_favorites'),
    path('ajax/generate-name/', views.generate_name_ajax, name='generate_name_ajax'),
    path("ajax/recent-names/", views.get_recent_names_ajax, name="get_recent_names_ajax"),
]