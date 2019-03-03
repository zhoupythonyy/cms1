
from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^cart/$', views.CartAddViem.as_view()),
    url(r'^cart/count/$', views.CartCountView.as_view()),
    url(r'^cart/selected_all/$', views.CartSelectedAllView.as_view()),

]
