from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Recruit section
    path('recruit', views.recruit, name='recruit'),
    path('recruit/signup', views.recruit_signup, name='recruit_signup'),
    path('recruit/<int:recruit_id>/trial', views.recruit_trial, name='recruit_trial'),
    path('recruit/success', views.recruit_success, name='recruit_success'),
    # Sith section
    path('sith', views.sith, name='sith'),
    path('sith/<int:recruit_id>/recruit', views.sith_recruit, name='sith_recruit'),
    #lists
    path('lists/all', views.lists_all, name='lists_all'),
    path('lists/more_than_one', views.lists_more_than_one, name='lists_more_than_one'),
]
