from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Post, Comment
from django.contrib import messages
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'  # Template to render the list
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'  # Template to render the category detail
    context_object_name = 'category'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category_form.html'  # Template to render the form for creating a category
    fields = ['name', 'description']

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category_form.html'  # Reuses the form template for updating
    fields = ['name', 'description']

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Post Views
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'  # Template to render the list of posts
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'  # Template to render a single post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'  # Template to render the form for creating a post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'  # Reuses the form template for updating
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_form.html'  # Template to render the form for creating a comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
