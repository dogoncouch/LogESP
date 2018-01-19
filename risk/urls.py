
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'risk'
urlpatterns = [
    path('', views.index, name='index'),
    path('ate/', views.ATEIndexView.as_view(), name='ate_index'),
    path('nte/', views.NTEIndexView.as_view(), name='nte_index'),
    path('ate/<int:pk>/', views.ATEDetailView.as_view(), name='ate_detail'),
    path('nte/<int:pk>/', views.NTEDetailView.as_view(), name='nte_detail'),
    path('ate/add/', login_required(views.ATECreateView.as_view()),
        name='ate_create'),
    path('nte/add/', login_required(views.NTECreateView.as_view()),
        name='nte_create'),
    path('ate/<int:pk>/update/', login_required(views.ATEUpdateView.as_view()),
        name='ate_update'),
    path('nte/<int:pk>/update/', login_required(views.NTEUpdateView.as_view()),
        name='nte_update'),
    #path('vuln/', views.VLIndexView.as_view(), name='vl_index'),
    #path('cond/', views.CNIndexView.as_view(), name='cn_index'),
    #path('vuln/<int:pk>/', views.VLDetailView.as_view(), name='vl_detail'),
    #path('cond/<int:pk>/', views.CNDetailView.as_view(), name='cn_detail'),
]

