from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Story, StoryStream
from .forms import NewStoryForm


@login_required
def new_story(request):
    user = request.user

    if request.method == "POST":
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('content')
            caption = form.cleaned_data.get('caption')
            story = Story(user=user, content=file, caption=caption)
            story.save()
            return redirect('post:index')
    else:
        form = NewStoryForm()

    context = {'form': form}

    return render(request, 'new_story.html', context)


def show_story(request, stream_id):
    stories = StoryStream.objects.get(id=stream_id)
    media = stories.story.all().values()
    stories_list = list(media)
    return JsonResponse(stories_list, safe=False)
