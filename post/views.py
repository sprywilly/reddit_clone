from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment
from .forms import CommentForm, AddPostForm


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post/post_list.html', {'page': page, 'posts': posts})


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post__id=post_id, approved=True)

    if request.method != 'POST':
        comment_form = CommentForm()

    else:
        comment_form = CommentForm(data=request.POST)
        parent_id = None
        try:
            parent_id = request.POST['comment_id']
        except:
            pass
        if comment_form.is_valid():
            print(request.POST)
            comment = comment_form.save(commit=False)
            comment.post = post
            if parent_id is not None:
                comment.parent = comments.get(id=parent_id)
            else:
                comment.parent = parent_id
            if request.user.is_authenticated:
                comment.author = request.user
                comment.approved = True
            else:
                comment.author = None

            comment.save()
            return HttpResponseRedirect(reverse('post:post_detail', args=[post_id]))

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments, }

    return render(request, 'post/post_detail.html', context)


def post_add(request):
    if request.POST:
        post_form = AddPostForm(request.POST)
        if post_form.is_valid():
            # post = post_form.cleaned_data
            post = post_form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
                post.is_published = True
            else:
                post.author = None
            post.save()

            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Произошла ошибка')
    else:
        post_form = AddPostForm()
    return render(request, 'post/post_add.html', {'post_form': post_form})
