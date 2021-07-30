from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('admin/', views.admin, name='admin'),
    path('middlemanager/<str:username>', views.middlemanager, name='middlemanager'),
    path('topmanager/<str:username>', views.topmanager, name='topmanager'),
    path('users/<str:username>', views.users, name='users'),
    path('rightsignin/<str:username>', views.rightsignin, name='rightsignin'),
    path('middlemanager_look/<str:username>', views.middlemanager_look, name='middlemanager_look'),
    path('topmanager_look/<str:username>', views.topmanager_look, name='topmanager_look'),
    path('error/<str:username>', views.error, name='error'),
]
