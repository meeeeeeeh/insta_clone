from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from .forms import NewPostForm
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from comment.forms import CommentForm
from stories.models import StoryStream
from django.db.models import Q


# class HomeView(ListView):
#     model = Post
#     template_name = 'index.html'
#     context_object_name = 'posts'
#
#     def get_queryset(self):
#         posts_ids = []
#         posts = Stream.objects.filter(user=self.request.user)
#         for post in posts:
#             posts_ids.append(post.post_id)
#         post_items = Post.objects.filter(id__in=posts_ids).all().order_by('-posted')
#         return post_items
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_ids = []
        posts = Stream.objects.filter(user=self.request.user)
        for post in posts:
            posts_ids.append(post.post_id)
        context['posts'] = Post.objects.filter(id__in=posts_ids).all().order_by('-posted')
        context['stories'] = StoryStream.objects.filter(user=self.request.user)
        return context


@login_required
def like(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
    post.likes = current_likes
    post.save()
    return redirect('post:post_detail', pk)


@login_required
def create_post(request):
    files_objs = []
    tags_objs = []
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files_list = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')
            tags_list = list(tags_form.split(','))
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            for file in files_list:
                f = PostFileContent(file=file, user=user)
                f.save()
                files_objs.append(f)

            post, created = Post.objects.get_or_create(user=user, caption=caption)
            post.tags.set(tags_objs)
            post.content.set(files_objs)
            post.save()
            return redirect('post:index')
    else:
        form = NewPostForm()

    context = {'form': form, }
    return render(request, 'post_create.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return redirect(reverse('post:post_detail', args=[pk]))
        else:
            return render(request, 'post_detail.html', {'comment_form': comment_form})
    else:
        comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'comment_form': comment_form,
               }
    return render(request, 'post_detail.html', context)


class TagsView(ListView):
    template_name = 'tag.html'
    model = Post
    context_object_name = 'posts'
    slug_url_kwarg = 'the_slug'

    def get_queryset(self, **kwargs):
        tag = get_object_or_404(Tag, slug=self.kwargs['the_slug'])
        return Post.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['the_slug'])
        return context


class ExploreView(TemplateView):
    template_name = 'explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['users'] = User.objects.filter(Q(username__icontains=query)) \
                .exclude(username=self.request.user.username)
        context['posts'] = Post.objects.all().order_by('-posted').exclude(user=self.request.user)
        return context
