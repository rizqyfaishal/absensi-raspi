from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'forward_data$', views.get_mac_address_data_from_raspi, name='get_mac_address_data_from_raspi'),
    url(r'konfirmasi/(?P<random_text>\w*)',views.konfirmasi_page, name='konfirmasi_page'),
    url(r'process_password$', views.process_konfirmasi_password, name='process_konfirmasi_password'),
   
    url(r'form$', views.form_registrasi, name='form_registrasi'),
    url(r'process_registrasi$', views.process_registrasi, name='process_registrasi')
]
