from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns=[
    path("",views.sign_in,name="login"),
    path('logout', views.signout,name='logout'),
    path("home",views.home,name="home"),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.list_orders, name='list_orders'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status')

]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)