from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard), 
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('jobs/new', views.newJobPage),
    path('jobs/new/create', views.createJob),
    path('jobs/<int:job_id>', views.viewJobPage),
    path('jobs/<int:job_id>/edit', views.editJobPage),
    path('jobs/<int:job_id>/update', views.updateJob),
    path('jobs/<int:job_id>/remove', views.removeJob),
]