from django.urls import path
from .views import sign_up_view, sign_in_view, logout_view, setting_view

urlpatterns = [
    path('signup/', sign_up_view),
    path('signin/', sign_in_view),
    path('logout/', logout_view),
    path('settings/', setting_view),

]
