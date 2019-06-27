from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('contacts/', views.contactList, name='contactlist'),
    path('contacts/new/', views.new_contact, name='new_contact'),
    path('contacts/<int:pk>/edit/', views.edit_contact, name='edit_contact'),
    path('contacts/<int:pk>/remove', views.delete_contact, name='delete_contact'),
    path('contacts/<int:pk>/delete', views.confirm_delete_contact, name='confirm_delete_contact'),
    path('contacts/upload', views.contact_upload, name='contact_upload'),
    path('contacts/export', views.contact_download, name='contact_download'),
    
]