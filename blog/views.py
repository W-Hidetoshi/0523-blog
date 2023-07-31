#cording:utf-8
#認証を行うメゾットをlogin_requiredからimport
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Comment,Category
from .forms import PostForm,CommentForm
#↑　from .form import PostFormはカレントディレクトリ内にあるform.pyからimportするという意味
#ここで、"."は"/"の意味。
from django.views.generic import ListView #検索およびページネーションを行うListView
from django.db.models import Q ,Count #Q:get_queryset()用の関数 Count:カウント用の関数
from django.contrib import messages #検索結果のメッセージ


class PostListView(ListView):
    context_object_name='post_list' #状態名
    template_name = 'blog/post_list.html'
    paginate_by = 5   #1ページに何件のレコードを表示させるか   
    model = Post
    
    def get_queryset(self, **kwargs):
        category_name = self.kwargs.get('category',None)   #URLのパラメータを辞書型でgetし、category_nameへ代入
        queryset = Post.objects.order_by('-created_date')  #作成日時を降順に並べ替えてソートする -#1   
        
        if category_name:            
            queryset = queryset.filter(category__name = category_name)  #少なくとも1つ以上の'category_name'を持つカテゴリ記事の情報をクエリする
            
        queryset = queryset.select_related('category')    
        
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|Q(text__icontains=query)
            )
            if len(query) > 100 :
                print("error")
                messages.add_message(self.request,messages.ERROR,'100文字以内で入力してください.')
            else :
                messages.add_message(self.request,messages.INFO,query)  #検索結果メッセージ
        queryset = queryset.annotate(cnt=Count('comments__id',filter=(Q(comments__approved_comment=1))))#|Q(comments__approved_comment=None))))

        return queryset
        
    # アクセスされた値を取得し辞書に格納
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs) 
        context['category_list'] = Category.objects.all()  #カテゴリー一覧をcontext['category_list']へデータを格納               
        category_name = self.kwargs.get('category',None)
        if category_name:
            context['category_key'] = self.kwargs['category']

        return context      
    
    

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
