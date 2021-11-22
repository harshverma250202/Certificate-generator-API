from django.contrib import admin
from django.urls import path
from app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('', views.index, name='index'),
    # path('certi/', views.certi, name='certi'),
    # path('pilcerti/', views.PILcerti, name='pilcerti'),
    path('ead_certificate_2021/',csrf_exempt(views.EadCertificateVIew.as_view()), name='ead_certificate_2021'),
    path('lsm_certificate_2021/',csrf_exempt(views.LsmCertificateVIew.as_view()), name='lsm_certificate_2021'),


 ]