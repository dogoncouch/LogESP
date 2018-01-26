
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'siem'
urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_index, name='event_index'),
    path('events/log/<int:pk>/', login_required(
        views.LogEventDetailView.as_view()), name='logevent_detail'),
    path('events/log/', login_required(
        views.LogEventSearchView.as_view()), name='logevent_search'),
    path('events/rule/', login_required(
        views.RuleEventSearchView.as_view()), name='ruleevent_search'),
    path('events/rule/<int:pk>/', login_required(
        views.RuleEventDetailView.as_view()), name='ruleevent_detail'),
    path('lr/', login_required(
        views.LRIndexView.as_view()), name='lr_index'),
    path('ph/', login_required(
        views.PHIndexView.as_view()), name='ph_index'),
    path('lr/<int:pk>/', login_required(
        views.LRDetailView.as_view()), name='lr_detail'),
    path('ph/<int:pk>/', login_required(
        views.PHDetailView.as_view()), name='ph_detail'),
    path('lr/add/', login_required(
        views.LRCreateView.as_view()), name='lr_create'),
    path('ph/add/', login_required(
        views.PHCreateView.as_view()), name='ph_create'),
    path('lr/<int:pk>/update/', login_required(
        views.LRUpdateView.as_view()), name='lr_update'),
    path('ph/<int:pk>/update/', login_required(
        views.PHUpdateView.as_view()), name='ph_update'),
    path('lr/<int:pk>/delete/', login_required(
        views.LRDeleteView.as_view()), name='lr_delete'),
    path('ph/<int:pk>/delete/', login_required(
        views.PHDeleteView.as_view()), name='ph_delete'),
]
