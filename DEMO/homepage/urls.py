from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup',views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    path('index',views.index, name="index"),
    path('booking',views.booking, name="booking"),
    path('check',views.check, name="check"),
    path('review',views.review, name="review")

]