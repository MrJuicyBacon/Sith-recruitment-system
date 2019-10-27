from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recruit', views.recruit, name='recruit'),
    path('recruit/signup', views.recruit_signup, name='recruit_signup'),
    path('recruit/<int:recruit_id>/trial', views.recruit_trial, name='recruit_trial'),
    path('recruit/success', views.recruit_success, name='recruit_success'),
]
