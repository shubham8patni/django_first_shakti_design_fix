import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, PostFormUpdate
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Upload


# Create your views here.
def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blogger/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blogger/home.html"  # <app></model>_<viewtype>.html
    context_object_name = "posts"
    # for date posted..by order of posting order
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blogger/user_posts.html"  # <app></model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostFormUpdate
    # fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blogger/about.html", {"title": "About"})


# @csrf_exempt
# def upload_image(request):
#     if request.method == "POST":
#         file_obj = request.FILES['file']
#         file_name_suffix = file_obj.name.split(".")[-1]
#         if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
#             return JsonResponse({"message": "Wrong file format"})

#         path = os.path.join(
#             settings.MEDIA_ROOT,
#             'tinymce',)

#         if not os.path.exists(path):
#             os.makedirs(path)

#         file_path = os.path.join(path, file_obj.name)
#         file_url = f'{settings.MEDIA_URL}tinymce/{file_obj.name}'

#         with open(file_path, 'wb+') as f:
#             for chunk in file_obj.chunks():
#                 f.write(chunk)

#         return JsonResponse({
#         'message': 'Image uploaded successfully',
#         'location' : file_url
#         })
#     return JsonResponse({'detail': "Wrong request"})

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['file']

#         file_name_suffix = uploaded_file.name.split(".")[-1]
#         if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
#             return JsonResponse({"message": "Wrong file format"})

#         fs = FileSystemStorage()
#         fs.location = os.path.join(
#             settings.MEDIA_ROOT,
#             'tinymce',)
#         name = fs.save(uploaded_file.name, uploaded_file)
#         url = fs.url(name)

#         return JsonResponse({
#             'message' : 'Upload Successful',
#             'location' : url
#         })
#     return JsonResponse({'details' : 'Uable to upload with current request'})

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        file_name_suffix = uploaded_file.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload = Upload(file = uploaded_file)
        upload.save()
        image_url = upload.file.url

        return JsonResponse({
            'message' : 'Upload Successful',
            'location' : image_url
        })
    return JsonResponse({'details' : 'Uable to upload with current request'})
        