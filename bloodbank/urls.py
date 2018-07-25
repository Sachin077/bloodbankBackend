from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
# from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from bloodbankApp import views 

urlpatterns = [
	path('admin/', admin.site.urls),
    #url(r'^admin/', include(admin.site.urls)),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('getUser/', views.getUser, name='getUser'),
    path('queryUsers/', views.queryUsers, name='queryUsers'),
    path('createRequest/', views.createRequest, name='createRequest'),
    path('updateRequest/', views.updateRequest, name='updateRequest'),
    path('deleteRequest/', views.deleteRequest, name='deleteRequest'),
    path('getRequestById/', views.getRequestById, name='getRequestById'),
    path('getRequestByUser/', views.getRequestByUser, name='getRequestByUser'),
    path('queryRequestForDonor/', views.queryRequestForDonor, name='queryRequestForDonor'),
    path('createResponse/', views.createResponse, name='createResponse'),
    path('getResponse/', views.getResponse, name='getResponse'),
    path('getResponsesByRequest/', views.getResponsesByRequest, name='getResponsesByRequest')
]