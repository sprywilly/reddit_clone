from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
#rom django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView

from .models import Post, Comment
from .forms import CommentForm, AddPostForm



class PostListView(ListView):
    """
    Выводит список опубликованных статей
    """
    queryset = Post.objects.filter(is_published=True).order_by('-created')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/post_list.html'


class CreatePost(FormView):
    """
    Вьюха добавления статьи
    """
    form_class = AddPostForm
    template_name = 'post/post_add.html'
    success_url = '/'


    def form_valid(self, form):
        instance = form.save(commit=False)

        # Если создал не аноним, то публикуем. Иначе на модерацию
        if self.request.user.is_authenticated:
            instance.author = self.request.user
            instance.is_published = True
        else:
            instance.author = None
        instance.save()
        return redirect(self.get_success_url())


def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)
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

