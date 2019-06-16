from django.urls import path
from .views import  add_user, employee_list, employee_detail, employee_edit, employee_delete

urlpatterns = [
	path('', employee_list, name='employee-list'),
	path('<int:id>', employee_detail, name='employee-detail'),
	path('<int:id>/edit', employee_edit, name='employee-edit'),
	path('<int:id>/delete', employee_delete, name='employee-delete'),
    path('add', add_user, name='add'),

]