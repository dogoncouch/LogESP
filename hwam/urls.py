
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'hwam'
urlpatterns = [
    path('', views.index, name='index'),
    path('ou/', views.OUIndexView.as_view(), name='ou_index'),
    path('hw/', views.HWIndexView.as_view(), name='hw_index'),
    path('sw/', views.SWIndexView.as_view(), name='sw_index'),
    path('ou/<int:pk>/', views.OUDetailView.as_view(), name='ou_detail'),
    path('hw/<int:pk>/', views.HWDetailView.as_view(), name='hw_detail'),
    path('sw/<int:pk>/', views.SWDetailView.as_view(), name='sw_detail'),
    path('ou/add/', login_required(views.OUCreateView.as_view()),
        name='ou_create'),
    path('hw/add/', login_required(views.HWCreateView.as_view()),
        name='hw_create'),
    path('sw/add/', login_required(views.SWCreateView.as_view()),
        name='sw_create'),
]

