from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


from .views import BookApprovalApiView, \
    BookManagementApiListView,\
    approve_book, \
    BookUploadApiView,\
    BookManagementApiDetailView,\
    CoverUploadApiView,\
    BookCommentApiListView,\
    approve_comment

app_name = "Library"
router = routers.DefaultRouter()
router.register(r'cover', CoverUploadApiView)

urlpatterns = [
    url(r'^book/approval/$', BookApprovalApiView.as_view()),
    url(r'^book/approve/$', approve_book),
    url(r'^book/document/$', BookUploadApiView.as_view()),
    url(r'^book/management/$', BookManagementApiListView.as_view()),
    url(r'^book/management/(?P<pk>\d+)', BookManagementApiDetailView.as_view()),
    url(r'^book/comment/(?P<pk>\d+)', BookCommentApiListView.as_view()),
    url(r'^book/comment/approve', approve_comment),
    url(r'^book/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
