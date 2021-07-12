from django.urls import path

from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:city_id>/', views.detail, name="detail"),
    path('api/now/', views.now, name="now"),
    path('api/min/', views.min, name="min"),
    path('api/max/', views.max, name="max"),
    path('api/avg/', views.avg, name="avg"),
    path('api/interval/', views.interval, name="interval"),
]
