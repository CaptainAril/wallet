from django.urls import include, path, re_path

from .views import (AuthServiceView, StatusView, UsersServiceView,
                    WalletServiceView)

urlpatterns = [
    path('status/', StatusView.as_view(), name='status'),
    # path('auth/', AuthServiceView.as_view(), name='auth_service'),
    re_path(r'^auth/(?P<path>.*)$', AuthServiceView.as_view(), name='auth_service'),
    re_path(r'^users/(?P<path>.*)$', UsersServiceView.as_view(), name='users_service'),
    re_path(r'^wallet/(?P<path>.*)$', WalletServiceView.as_view(), name='wallet_service'),
]
