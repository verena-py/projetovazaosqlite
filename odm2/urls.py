
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.paginainicial, name='paginainicial'),
    path('projeto/', views.projeto, name='projeto'),
    path('dados/', views.dados, name='dados'),
    path('mapa/', views.mapa, name='mapa'),
    path('analise/', views.analise, name='analise'),
    path('gantt/', views.gantt, name='gantt'),
    path('hidro/', views.hidro, name='hidro'),
    path('disp/', views.disp, name='disp'),
    path('histo/', views.histo, name='histo'),
    path('box/', views.box, name='box'),


]