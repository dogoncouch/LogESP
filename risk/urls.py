
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'risk'
urlpatterns = [
    path('', views.index, name='index'),
    path('ate/', views.ATEIndexView.as_view(), name='ate_index'),
    path('nte/', views.NTEIndexView.as_view(), name='nte_index'),
    path('ats/', views.ATSIndexView.as_view(), name='ats_index'),
    path('nts/', views.NTSIndexView.as_view(), name='nts_index'),
    path('ate/<int:pk>/', views.ATEDetailView.as_view(), name='ate_detail'),
    path('nte/<int:pk>/', views.NTEDetailView.as_view(), name='nte_detail'),
    path('ats/<int:pk>/', views.ATSDetailView.as_view(), name='ats_detail'),
    path('nts/<int:pk>/', views.NTSDetailView.as_view(), name='nts_detail'),
    path('ate/add/', login_required(views.ATECreateView.as_view()),
        name='ate_create'),
    path('nte/add/', login_required(views.NTECreateView.as_view()),
        name='nte_create'),
    path('ats/add/', login_required(views.ATSCreateView.as_view()),
        name='ats_create'),
    path('nts/add/', login_required(views.NTSCreateView.as_view()),
        name='nts_create'),
    path('ate/<int:pk>/update/', login_required(views.ATEUpdateView.as_view()),
        name='ate_update'),
    path('nte/<int:pk>/update/', login_required(views.NTEUpdateView.as_view()),
        name='nte_update'),
    path('ats/<int:pk>/update/', login_required(views.ATSUpdateView.as_view()),
        name='ats_update'),
    path('nts/<int:pk>/update/', login_required(views.NTSUpdateView.as_view()),
        name='nts_update'),
    #path('vuln/', views.VLIndexView.as_view(), name='vl_index'),
    #path('cond/', views.CNIndexView.as_view(), name='cn_index'),
    #path('vuln/<int:pk>/', views.VLDetailView.as_view(), name='vl_detail'),
    #path('cond/<int:pk>/', views.CNDetailView.as_view(), name='cn_detail'),
]

