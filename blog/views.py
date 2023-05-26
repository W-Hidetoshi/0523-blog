#cording:utf-8
#認証を行うメゾットをlogin_requiredからimport
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Comment
from .forms import PostForm,CommentForm
#↑　from .form import PostFormはカレントディレクトリ内にあるform.pyからimportするという意味
#ここで、"."は"/"の意味。
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
'''
class PostListView(ListView):
    model = post_list
    template_name = 'post_list.html'
    paginate_by = 10    #一度に表示するレコード数
'''

def post_list(request):
    posts = Post.objects.order_by('created_date').reverse()
    #context ={'pages': pages}
    #context_post = {'posts': posts}
    paginator = Paginator(posts,3)
    page_num = request.GET.get('page',1)

    try:
        pages = paginator.page(page_num)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
    #context_page ={'pages': pages} 
   
    return render(request, 'blog/post_list.html', {'pages':pages,'posts':posts})

'''
def post_index(request):
    Posts_a = Post.objects.order_by('created_date').reverse()
    paginator = Paginator(Posts_a,2)
    page = request.GET.get('page',1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
    context ={'pages': pages}
    return render(request, 'blog/templates/blog/base.html',context)
'''

@login_required  #login_required：ログイン後に操作ができる関数（以降同様）
#新規記事投稿
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)      
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form': form})

@login_required
#記事編集
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
        else:
            return render(request, 'blog/post_edit.html',{'form':form})
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html',{'posts': posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)    #postにget_object(データがある場合)もしくは404（URLが見つからない場合）を入れる
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#コメント承認
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

#コメント削除
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
