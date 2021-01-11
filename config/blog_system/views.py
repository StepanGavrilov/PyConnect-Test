from django.http import HttpResponse

from .forms import PostCreateForm
from .forms import CommentCreateForm

from .models import Post
from .models import Comment


from django.shortcuts import render, redirect
from django.views import generic

from .base.permissions import IsAuthorEntry


class CreatePostView(generic.CreateView):
    """
    Создание поста
    """

    model = Post
    form_class = PostCreateForm

    def get(self, request, *args, **kwargs):
        print('Here')
        return render(request, 'blog/post_create.html', {'post_create_form': PostCreateForm})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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
    queryset = Post.objects.all()

    def get_queryset(self):
        if self.queryset is None:
            return None
        return self.queryset

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        return render(request, 'blog/post_wall.html', {'posts': posts})


class PostDetailView(generic.DetailView):
    """
    Детальный пост с комментариями
    """

    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        print('DetailView')
        print(kwargs, '\n\n\n')
        post = Post.objects.get(id=kwargs['id'])
        comments = Comment.objects.filter(post=kwargs['id'])
        return self.render_to_response({'post': post,
                                        'comments': comments,
                                        'comment_form': CommentCreateForm})


class PostDeleteView(generic.DeleteView):
    """
    Удаление поста автором
    """
    model = Post

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        Post.delete(post)
        return redirect('blog_system:posts_wall')


class CommentCreateView(generic.CreateView):
    """
    Создание комментрания
    """

    model = Comment
    form_class = CommentCreateForm

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            print('\nValid\n')
            comment = Comment()
            comment.author = request.user
            comment.post = post
            comment.text = form.cleaned_data['text']
            comment.save()

            return redirect('account_system:friends')
        return HttpResponse('<h1>not valid!</h1>')


