from django.shortcuts import render
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post
from .forms import PostForm

# Create your views here.


class IndexView(TemplateView):
    """
    a lower lvl class based view to generate a simple index view
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = "admin"
        context["posts"] = Post.objects.all()
        return context


class PostListView(ListView):
    queryset = Post.objects.filter(status=True)
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    # model = Post
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
    success_url = "blog/posts/"
    permission_required = "blog.view_post"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/posts/"
    template_name = "blog/post_create.html"
    permission_required = "blog.change_post"


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/posts/"
    permission_required = "blog.delete_post"
