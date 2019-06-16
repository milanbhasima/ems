from django.urls import path
from .views import index,detail,poll,addpoll,editpoll,deletepoll

urlpatterns = [
    path('', index, name='index'),
    path('add/', addpoll, name='add-poll'),
    path('<int:id>/edit/', editpoll, name='edit'),
    path('<int:id>/delete/', deletepoll, name='delete'),
    path('<int:id>', poll, name='poll'),
    path('<int:id>/detail', detail, name='detail'),
]