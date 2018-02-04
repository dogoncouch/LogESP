
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'siem'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('events/', login_required(views.event_index), name='event_index'),
    path('events/log/<int:pk>/', login_required(
        views.LogEventDetailView.as_view()), name='logevent_detail'),
    path('events/log/', login_required(
        views.LogEventSearchView.as_view()), name='logevent_search'),
    path('events/rule/', login_required(
        views.RuleEventSearchView.as_view()), name='ruleevent_search'),
    path('events/rule/<int:pk>/', login_required(
        views.RuleEventDetailView.as_view()), name='ruleevent_detail'),
    path('rules/limit/', login_required(
        views.LRIndexView.as_view()), name='lr_index'),
    path('rules/limit/<int:pk>/', login_required(
        views.LRDetailView.as_view()), name='lr_detail'),
    path('rules/limit/add/', login_required(
        views.LRCreateView.as_view()), name='lr_create'),
    path('rules/limit/<int:pk>/update/', login_required(
        views.LRUpdateView.as_view()), name='lr_update'),
    path('rules/limit/<int:pk>/delete/', login_required(
        views.LRDeleteView.as_view()), name='lr_delete'),
    path('parsers/log/', login_required(
        views.LPIndexView.as_view()), name='lp_index'),
    path('parsers/log/<int:pk>/', login_required(
        views.LPDetailView.as_view()), name='lp_detail'),
    path('parsers/log/add/', login_required(
        views.LPCreateView.as_view()), name='lp_create'),
    path('parsers/log/<int:pk>/update/', login_required(
        views.LPUpdateView.as_view()), name='lp_update'),
    path('parsers/log/<int:pk>/delete/', login_required(
        views.LPDeleteView.as_view()), name='lp_delete'),
]
