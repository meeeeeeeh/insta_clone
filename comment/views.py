from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy, reverse
from post.models import Post
from django.shortcuts import get_object_or_404
from authentification.models import Profile


def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    comments = Comment.objects.filter(post=post).order_by('date')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = user
            comments.save()
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


class CommentView(ListView):
    model = Comment
    template_name = 'post_detail.html'
    context_object_name = 'comments'
