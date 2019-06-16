from django.contrib import admin
from django.urls import path, include
from employee.views import user_login, user_logout,success, MyProfile, MyProfileUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll/', include('poll.urls')),
    path('employee/', include('employee.urls')),
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('success', success, name='success'),
    path('profile', MyProfile.as_view(), name='profile'),
    path('profile/update/', MyProfileUpdate.as_view(), name='update'),
]