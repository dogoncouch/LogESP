
from django.urls import path

from . import views

app_name = 'risk'
urlpatterns = [
    path('', views.index, name='index'),
    path('ate/', views.ATEIndexView.as_view(), name='ate_index'),
    path('nte/', views.NTEIndexView.as_view(), name='nte_index'),
    path('ate/<int:pk>/', views.ATEDetailView.as_view(), name='ate_detail'),
    path('nte/<int:pk>/', views.NTEDetailView.as_view(), name='nte_detail'),
    #path('advthreat/', views.ATIndexView.as_view(), name='at_index'),
    #path('nathreat/', views.NTIndexView.as_view(), name='nt_index'),
    #path('threatevt/', views.TEIndexView.as_view(), name='te_index'),
    #path('vuln/', views.VLIndexView.as_view(), name='vl_index'),
    #path('cond/', views.CNIndexView.as_view(), name='cn_index'),
    #path('advthreat/<int:pk>/', views.ATDetailView.as_view(), name='at_detail'),
    #path('nathreat/<int:pk>/', views.NTDetailView.as_view(), name='nt_detail'),
    #path('threatevt/<int:pk>/', views.TEDetailView.as_view(), name='te_detail'),
    #path('vuln/<int:pk>/', views.VLDetailView.as_view(), name='vl_detail'),
    #path('cond/<int:pk>/', views.CNDetailView.as_view(), name='cn_detail'),
]

