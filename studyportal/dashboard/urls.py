from django.contrib import admin
from django.urls import path
from . import views

app_name="dashboard"
urlpatterns=[
    path('',views.index,name="index"),
   path('user_home',views.user_home,name="user_home"),
   path('admin_home',views.admin_home,name="admin_home"), 
   path("forum", views.forum, name="forum"),
   path("discussion/<int:myid>", views.discussion, name="discussion"),
   path("showallusers", views.show_all_users, name="showallusers"),
   path('delete_user/<int:pk>',views.delete_user,name="delete_user"),
   path('delete_post/<int:pk>',views.delete_post,name="delete_post"),
    path('delete_reply/<int:pk>',views.delete_reply,name="delete_reply"),
 path('upload_notes', views.upload_notes, name='upload_notes'),
 path('view_mynotes', views.view_mynotes, name='view_mynotes'),
 path('delete_mynotes/<int:pk>/', views.delete_mynotes, name='delete_mynotes'),
 path('pending_notes', views.pending_notes, name='pending_notes'),
path('assign_status/<int:pk>', views.assign_status, name='assign_status'),
path('accepted_notes', views.accepted_notes, name='accepted_notes'),
path('rejected_notes', views.rejected_notes, name='rejected_notes'),
path('all_notes', views.all_notes, name='all_notes'),
 path('delete_notes/<int:pk>', views.delete_notes, name='delete_notes'),
path('delete-records/', views.delete_notes, name='delete_notes'),
path('view_allnotes', views.view_allnotes, name='view_allnotes'),
path('notessharing', views.notessharing, name='notessharing'),
path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
path('edit_reply/<int:pk>/', views.edit_reply, name='edit_reply'),

 ]