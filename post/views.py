from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()

    return render(request, 'post/post_list.html', {'posts':posts})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    return render(request,'post/post_detail.html', {'post':post})
