from django.conf.urls import url
from .views import (LoginView, RegistroView)

urlpatterns = [
    url(r'^$', LoginView.as_view(),
        name='login'),
    url(r'^login/$', LoginView.as_view(),
        name='login'),
    url(r'^cadastro/$', RegistroView.as_view(),
        name='cadastro'),
]
