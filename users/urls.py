from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',views.UserView.as_view(), name="user_list_view"),
    path('signup/', views.UserView.as_view(), name="user_view"),
    path('mock/', views.mockView.as_view(), name = "mock_view"),
    path('<int:user_id>/', views.UserInformationView.as_view(), name="user_information_view"),
    path('myuser/', views.UserInformationView.as_view(), name="myuser_view"),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]