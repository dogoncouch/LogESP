
from django.urls import path

from . import views

app_name = 'hwam'
urlpatterns = [
    path('', views.index, name='index'),
    path('ou/', views.OUIndexView.as_view(), name='ou_index'),
    path('hw/', views.HWIndexView.as_view(), name='hw_index'),
    path('sw/', views.SWIndexView.as_view(), name='sw_index'),
    path('ou/<int:organizational_unit_id>/', views.ou_detail,
        name='ou_detail'),
    path('hw/<int:hardware_asset_id>/', views.hw_detail,
        name='hw_detail'),
    path('sw/<int:software_asset_id>/', views.sw_detail,
        name='sw_detail'),
]

