from django.urls import path
from .  import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('register/api', views.User_regiter.as_view(), name="register/api" ),
    path('user_login', views.user_login.as_view(), name="user_login"),
    path('api/create_shorturl', views.create_shorterend_url.as_view(), name="api/create_shorturl"),
    path("create_qr/<int:id>", views.find_user, name="create_qr"),
    path('view_user', views.view_user.as_view(), name="view_user"),
    path('update_url', views.update_url.as_view(), name="update_url"),
    path("view_url", views.view_url.as_view(), name="view_url"),
    path('delete_url', views.delete_url.as_view(), name="delete_url"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('show_user_details', views.show_user_details.as_view(), name="show_user_details")
]
