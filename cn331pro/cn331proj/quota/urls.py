from django.urls import path
from quota import views 
from users import views as uv

urlpatterns = [
    path('', views.index,name='home'),
    path('subject_list', views.subject_list,name='subject_list'),
    path('my_quota', views.my_quota, name='my_quota'),
    path('add_subject/<id>', views.add_subject,name='add_subject'),
    path('del_subject/<id>', views.del_subject,name='del_subject'),
]