from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserViewSet.as_view({'get': 'list'}), name='list'),
    path('autocomplete/', views.UserViewSet.as_view({'get': 'autocomplete'}), name='autocomplete'),
]
