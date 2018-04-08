
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'siem'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('help/', login_required(views.help_index), name='help_index'),
    path('help/parsing/', login_required(views.parse_help),
        name='parse_help'),
    path('help/rules/', login_required(views.rule_help),
        name='rule_help'),
    path('help/events/', login_required(views.event_help),
        name='event_help'),
    path('help/daemons/', login_required(views.daemon_help),
        name='daemon_help'),
    path('help/regex/', login_required(views.regex_help),
        name='regex_help'),
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
    path('parsers/helpers/', login_required(
        views.PHIndexView.as_view()), name='ph_index'),
    path('parsers/helpers/<int:pk>/', login_required(
        views.PHDetailView.as_view()), name='ph_detail'),
    path('parsers/helpers/add/', login_required(
        views.PHCreateView.as_view()), name='ph_create'),
    path('parsers/helpers/<int:pk>/update/', login_required(
        views.PHUpdateView.as_view()), name='ph_update'),
    path('parsers/helpers/<int:pk>/delete/', login_required(
        views.PHDeleteView.as_view()), name='ph_delete'),
]
