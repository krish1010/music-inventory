from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init', views.init, name='init'),
    path('search/', views.search, name='search'),
    path('add_to_cart/<int:music_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/<int:music_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:music_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('search/view_cart', views.view_cart, name='view_cart'),
    path('send_mail', views.send_mail, name='send_mail'),
    path('<str:genre>', views.genre_view, name='genre_view'),
]
