from . import views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name="logout"),

    #cart
    path('excel/', views.excel, name='excel'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('submit/<int:id>/', views.submit, name='submit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)