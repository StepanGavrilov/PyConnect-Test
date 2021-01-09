from django.http import HttpResponse

from .forms import PostCreateForm
from .models import Post


from django.shortcuts import render, redirect
from django.views import generic


class CreatePostView(generic.CreateView):
    """
    Создание поста
    """

    model = Post
    form_class = PostCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, 'blog/post_create.html', {'post_create_form': PostCreateForm})

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = Post()
            post.owner = request.user
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.save()
            return redirect('account_system:friends')
        return HttpResponse('<h1>not valid!</h1>')


class PostWallView(generic.ListView):
    """
    Лента постов
    """
    queryset = Post.objects.order_by('-last_update')

    def get_queryset(self):
        if self.queryset is None:
            return None
        return self.queryset

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        return render(request, 'blog/post_wall.html', {'posts': posts})
