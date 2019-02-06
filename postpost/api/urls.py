from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.UserRegistration.as_view(), name='users_registration'),
    path('publications/', views.PublicationList.as_view(), name='publications_list'),
    path('publications/<int:pk>', views.Publication.as_view(), name='publications_details'),
]
