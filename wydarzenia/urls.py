from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login_page/", views.login_page, name="login_page"),
    path("logout/", views.logout_user, name="logout"),
    path("register_page/", views.register_page, name="register_page"),
    path("", views.home, name="home"),
    path("room/<int:pk>/", views.room, name="room"),
    # path("profile/<int:pk>", views.user_profile, name="user-profile"),
    path("create-room/", views.create_room, name="create-room"),
    # path("profile/<int:pk>/", views.user_profile, name="user-profile"),
    path("update-room/<int:pk>/", views.update_room, name="update-room"),
    path("delete-room/<int:pk>/", views.delete_room, name="delete-room"),
    path("history/", views.history, name="history"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path("delete-message/<int:pk>/", views.delete_message, name="delete-message"),
]
