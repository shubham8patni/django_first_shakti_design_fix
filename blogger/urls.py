from django.urls import include, path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    # path("", views.home, name="blogger-home"),
    path("", PostListView.as_view(), name="blogger-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path("about/", views.about, name="blogger-about"),
    path('tinymce/', include('tinymce.urls')),
    path('upload_image/', views.upload_image),
]


# <app></model>_<viewtype>.html
