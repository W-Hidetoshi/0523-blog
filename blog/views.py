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
from django.db.models import Q #get_queryset()用の関数
from django.contrib import messages #検索結果のメッセージ
'''
class IndexView(ListView):
    model = Post
    template_name = 'blog/post_contents_list.html'
    paginate_by = 5   #ページング件数
     
    def get_queryset(self):
        #queryset = Post.objects.order_by('-created_date')
        queryset = Post.objects.order_by('-id')
        return queryset
'''
'''    
# カテゴリー一覧   
class CategoryView(ListView):
    model = Post
    template_name = 'blog/post_contents_list.html' 
    #template_name = 'blog/post_list.html'
    paginate_by = 5   #ページング件数 
    
    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        #queryset = Post.objects.order_by('-created_data').filter(category=category)
        queryset = Post.objects.order_by('-id').filter(category=category)
        return queryset

    # アクセスされた値を取得し辞書に格納
    def get_context_data(self,**kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['category_key'] = self.kwargs['category']
        return context
'''

class PostListView(ListView):
    context_object_name='post_list' #状態名
    # queryset = Post.objects.order_by('-created_date')
    template_name = 'blog/post_list.html'
    paginate_by = 5   #1ページに何件のレコードを表示させるか
    model = Post
    
    def get_queryset(self, **kwargs):
        category_name = self.kwargs.get('category',None)
        print(category_name)  
        print(self.kwargs.get('category')) 
        
        if category_name == None:
            queryset = Post.objects.order_by('-created_date')
            
        elif category_name == self.kwargs.get('category'):
            print(category_name)
            category = Category.objects.get(name=self.kwargs['category'])
            queryset = Post.objects.order_by('-created_date').filter(category=category)
            #return queryset
        
       
        #queryset = Post.objects.order_by('-created_date')
        
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|Q(text__icontains=query)
            )
            if len(query) > 100 :
                print("error")
                messages.add_message(self.request,messages.ERROR,'100文字以内で入力してください.')
                #messages.error(self.request,'100文字以内で入力してください。')
            else :
                messages.add_message(self.request,messages.INFO,query)  #検索結果メッセージ
        
        return queryset
        
    # アクセスされた値を取得し辞書に格納
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category',None)
        
        print(category_name)
        
        if category_name==None:
            pass
        elif category_name == self.kwargs.get('category'):
            print(category_name) 
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
