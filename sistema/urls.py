from django.conf.urls import url

from sistema.views import signup

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
]
