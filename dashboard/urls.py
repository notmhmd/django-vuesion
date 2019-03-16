from django.conf.urls import url
from django.urls import include
from .views import UserListApiView, UserDetailsView


app_name = "Dashboard"
urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration', include('rest_auth.registration.urls')),
    url(r'^user/$', UserListApiView.as_view()),
    url(r'^user/(?P<pk>\d+)', UserDetailsView.as_view()),
]
