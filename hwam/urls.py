
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'hwam'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('help/', login_required(views.help_index), name='help_index'),
    path('ou/', login_required(views.OUIndexView.as_view()),
        name='ou_index'),
    path('hw/', login_required(views.HWIndexView.as_view()),
        name='hw_index'),
    path('sw/', login_required(views.SWIndexView.as_view()),
        name='sw_index'),
    path('hw/search/', login_required(views.HWSearchView.as_view()),
        name='hw_search'),
    path('sw/search/', login_required(views.SWSearchView.as_view()),
        name='sw_search'),
    path('ou/<int:pk>/', login_required(views.OUDetailView.as_view()),
        name='ou_detail'),
    path('hw/<int:pk>/', login_required(views.HWDetailView.as_view()),
        name='hw_detail'),
    path('sw/<int:pk>/', login_required(views.SWDetailView.as_view()),
        name='sw_detail'),
    path('ou/add/', login_required(views.OUCreateView.as_view()),
        name='ou_create'),
    path('hw/add/', login_required(views.HWCreateView.as_view()),
        name='hw_create'),
    path('sw/add/', login_required(views.SWCreateView.as_view()),
        name='sw_create'),
    path('ou/<int:pk>/update/', login_required(views.OUUpdateView.as_view()),
        name='ou_update'),
    path('hw/<int:pk>/update/', login_required(views.HWUpdateView.as_view()),
        name='hw_update'),
    path('sw/<int:pk>/update/', login_required(views.SWUpdateView.as_view()),
        name='sw_update'),
    path('ou/<int:pk>/delete/', login_required(
        views.OUDeleteView.as_view()), name='ou_delete'),
    path('hw/<int:pk>/delete/', login_required(
        views.HWDeleteView.as_view()), name='hw_delete'),
    path('sw/<int:pk>/delete/', login_required(
        views.SWDeleteView.as_view()), name='sw_delete'),
]

